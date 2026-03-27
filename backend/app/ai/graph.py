from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.ai.state import EngineeringState
from app.ai.agents.phase1_functional import phase1_generator, phase1_validator
from app.ai.agents.phase2_morphology import phase2_generator, phase2_validator
from app.ai.agents.phase3_risk import phase3_generator, phase3_validator

def route_based_on_phase(state: EngineeringState):
    phase = state.get("current_phase")
    if phase == "functional_decomposition":
        return "generate_phase1"
    elif phase == "morphological_chart":
        return "generate_phase2"
    elif phase == "risk_analysis":
        return "generate_phase3"
    return END

# --- Phase 1 Nodes ---
def generate_phase1(state: EngineeringState):
    tree = phase1_generator.invoke({
        "problem_statement": state["problem_statement"],
        "validation_feedback": state.get("validation_feedback", "")
    })
    return {"functional_tree": tree.dict(), "revision_count": 1}

def validate_phase1(state: EngineeringState):
    res = phase1_validator.invoke({"functional_tree": json.dumps(state["functional_tree"])})
    if res.is_valid:
        return {"validation_feedback": ""}
    else:
        return {"validation_feedback": res.feedback}

def check_validity_phase1(state: EngineeringState):
    if state.get("validation_feedback"):
        if state.get("revision_count", 0) >= 3:
            return END
        return "generate_phase1"
    return END

# --- Phase 2 Nodes ---
def generate_phase2(state: EngineeringState):
    logger.info("Starting Phase 2 generation")
    
    if not state.get("functional_tree"):
        raise ValueError("Cannot run Phase 2: Functional tree is missing from state.")

    # Simple retry logic for LLM call
    last_error = None
    for attempt in range(2):
        try:
            chart = phase2_generator.invoke({
                "functional_tree": json.dumps(state["functional_tree"]),
                "validation_feedback": state.get("validation_feedback", "")
            })
            if not chart or not chart.mappings:
                raise ValueError("LLM returned empty morphological chart")
            
            logger.info("Successfully generated Phase 2 morphological chart")
            return {"morphological_alternatives": chart.dict(), "revision_count": 1}
        except Exception as e:
            logger.warning(f"Phase 2 generation attempt {attempt + 1} failed: {str(e)}")
            last_error = e
            
    logger.error(f"Phase 2 generation failed after all attempts: {str(last_error)}")
    raise last_error

def validate_phase2(state: EngineeringState):
    if not state.get("morphological_alternatives"):
        return {"validation_feedback": "Error: No morphological chart to validate."}
        
    try:
        res = phase2_validator.invoke({"morphological_chart": json.dumps(state["morphological_alternatives"])})
        if res.is_valid:
            return {"validation_feedback": ""}
        else:
            return {"validation_feedback": res.feedback}
    except Exception as e:
        logger.error(f"Phase 2 validation failed: {str(e)}")
        # In case of validation failure, we might want to just proceed or try again. 
        # For now, we return the error as feedback to trigger a retry in the graph if possible.
        return {"validation_feedback": f"Validation error: {str(e)}"}

def check_validity_phase2(state: EngineeringState):
    if state.get("validation_feedback"):
        if state.get("revision_count", 0) >= 3:
            return END
        return "generate_phase2"
    return END

# --- Phase 3 Nodes ---
def generate_phase3(state: EngineeringState):
    logger.info("Starting Phase 3 generation")
    all_items = []
    morph = state.get("morphological_alternatives", {})
    
    if not morph:
        raise ValueError("Cannot run Phase 3: Morphological alternatives are missing.")
        
    mappings = morph.get("mappings", [])
    
    # Fallback if the dict structure is different
    if isinstance(morph, list):
        mappings = morph
    elif not mappings and isinstance(morph, dict):
        # Check if the whole object is a list under a different key or if it's the list itself
        for key, value in morph.items():
            if isinstance(value, list) and len(value) > 0:
                mappings = value
                break
                
    if not mappings:
        logger.error(f"No mappings found in morphological alternatives: {morph}")
        raise ValueError("Morphological chart is empty or incorrectly formatted. Please rerun Phase 2.")
        
    logger.info(f"Processing {len(mappings)} functions for Phase 3")
    
    for mapping in mappings:
        func_name = mapping.get("function", "")
        alts = mapping.get("solutions", [])
        
        if not func_name or not alts:
            logger.warning(f"Skipping incomplete mapping: {mapping}")
            continue

        # Retry logic for each function's SWOT analysis
        func_res = None
        for attempt in range(2):
            try:
                res = phase3_generator.invoke({
                    "problem_statement": state.get("problem_statement", ""),
                    "functional_tree": json.dumps(state.get("functional_tree", {})),
                    "function_name": func_name,
                    "alternatives": json.dumps(alts),
                    "validation_feedback": state.get("validation_feedback", "")
                })
                if res and hasattr(res, 'analysis'):
                    all_items.extend(res.analysis)
                    func_res = res
                    break
                else:
                    raise ValueError(f"Phase 3 LLM returned invalid result for function {func_name}")
            except Exception as e:
                logger.warning(f"Phase 3 generation for function {func_name} attempt {attempt + 1} failed: {str(e)}")
        
        if not func_res:
            logger.error(f"Failed to generate SWOT for function {func_name} after all attempts.")

    if not all_items:
        raise ValueError("Phase 3 failed to generate any SWOT analysis items. Check LLM availability and inputs.")

    items_dicts = [item.dict() for item in all_items]
    logger.info(f"Successfully generated Phase 3 with {len(items_dicts)} items")
    return {"risk_checklist": {"items": items_dicts}, "revision_count": 1}

def validate_phase3(state: EngineeringState):
    if not state.get("risk_checklist"):
        return {"validation_feedback": "Error: No risk checklist to validate."}
        
    try:
        res = phase3_validator.invoke({
            "morphological_alternatives": json.dumps(state.get("morphological_alternatives", {})),
            "risk_checklist": json.dumps(state["risk_checklist"])
        })
        if res.is_valid:
            return {"validation_feedback": ""}
        else:
            return {"validation_feedback": res.feedback}
    except Exception as e:
        logger.error(f"Phase 3 validation failed: {str(e)}")
        return {"validation_feedback": f"Validation error: {str(e)}"}

def check_validity_phase3(state: EngineeringState):
    if state.get("validation_feedback"):
        if state.get("revision_count", 0) >= 3:
            return END
        return "generate_phase3"
    return END


# --- Graph Construction ---
workflow = StateGraph(EngineeringState)

# Add nodes
workflow.add_node("generate_phase1", generate_phase1)
workflow.add_node("validate_phase1", validate_phase1)

workflow.add_node("generate_phase2", generate_phase2)
workflow.add_node("validate_phase2", validate_phase2)

workflow.add_node("generate_phase3", generate_phase3)
workflow.add_node("validate_phase3", validate_phase3)

# Add edges
workflow.add_conditional_edges(START, route_based_on_phase)

# Phase 1 loop
workflow.add_edge("generate_phase1", "validate_phase1")
workflow.add_conditional_edges("validate_phase1", check_validity_phase1, {"generate_phase1": "generate_phase1", END: END})

# Phase 2 loop
workflow.add_edge("generate_phase2", "validate_phase2")
workflow.add_conditional_edges("validate_phase2", check_validity_phase2, {"generate_phase2": "generate_phase2", END: END})

# Phase 3 loop
workflow.add_edge("generate_phase3", "validate_phase3")
workflow.add_conditional_edges("validate_phase3", check_validity_phase3, {"generate_phase3": "generate_phase3", END: END})

# Setup Memory Checkpointer
memory = MemorySaver()

# Compile graph with human-in-the-loop breakpoints (interrupt_after)
# We interrupt after validation if it's successful (returning END from condition means it reaches END of phase processing)
# We can set interrupt_after=["validate_phase1", "validate_phase2", "validate_phase3"] for breakpoints
# Actually, since these nodes conditionally go to END if valid (or max retries), we can just set interrupt_after the validate nodes.
# When the subgraph finishes, the API waits for user input before proceeding to the next phase, which is done via API calls setting the `current_phase`.
app_graph = workflow.compile(checkpointer=memory, interrupt_after=["validate_phase1", "validate_phase2", "validate_phase3"])
