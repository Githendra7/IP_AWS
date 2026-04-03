import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List, Dict

from app.core.config import settings
from app.ai.tools.taxonomies import Functional_Basis_Lookup, TRIZ_Principles_Query
from app.ai.agents.validators import ValidationResult

class SubSubFunction(BaseModel):
    function: str = Field(description="Level 3 abstract engineering function (Verb + Noun). e.g., 'remove material' or 'store data'.")
    material_flow: str = Field(description="Flow of material (e.g. physical objects, substances). For software-only, this may be structural data entities, datasets, or 'N/A'.")
    energy_flow: str = Field(description="Flow of energy (e.g. electrical, mechanical, human). For software-only, this may be compute execution, triggers, or 'N/A'.")
    information_flow: str = Field(description="Flow of information (e.g. control system, sensors, signals, data payloads, logical states).")

class SubFunction(BaseModel):
    function: str = Field(description="Level 2 abstract engineering function (Verb + Noun). e.g., 'remove material' or 'store data'.")
    material_flow: str = Field(description="Flow of material (e.g. physical objects, substances). For software-only, this may be structural data entities, datasets, or 'N/A'.")
    energy_flow: str = Field(description="Flow of energy (e.g. electrical, mechanical, human). For software-only, this may be compute execution, triggers, or 'N/A'.")
    information_flow: str = Field(description="Flow of information (e.g. control system, sensors, signals, data payloads, logical states).")
    sub_sub_functions: List[SubSubFunction] = Field(default_factory=list, description="Child sub-sub-functions for this Level 2 function.")

class MainFunction(BaseModel):
    function: str = Field(description="Level 1 abstract engineering function (Verb + Noun).")
    material_flow: str = Field(description="Flow of material (e.g. physical objects, substances). For software-only, this may be structural data entities, datasets, or 'N/A'.")
    energy_flow: str = Field(description="Flow of energy (e.g. electrical, mechanical, human). For software-only, this may be compute execution, triggers, or 'N/A'.")
    information_flow: str = Field(description="Flow of information (e.g. control system, sensors, signals, data payloads, logical states).")
    sub_functions: List[SubFunction] = Field(default_factory=list, description="Child sub-functions for this Level 1 function.")

class FunctionalTree(BaseModel):
    root_function: str = Field(description="The main top-level function of the system (Verb + Noun).")
    material_flow: str = Field(description="Flow of material at the system level. (Can be 'N/A' for pure software).")
    energy_flow: str = Field(description="Flow of energy at the system level. (Can be 'N/A' for pure software).")
    information_flow: str = Field(description="Flow of information at the system level.")
    main_functions: List[MainFunction] = Field(description="The Level 1 functions that decompose the root function.")

# Generator
generator_llm = ChatGroq(temperature=0.7, model_name="llama-3.3-70b-versatile", groq_api_key=settings.GROQ_API_KEY, max_retries=6)

generator_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a Functional Architect specializing in engineering system abstraction across hardware, software, and hybrid domains. Your task is to perform an expert-level Functional Decomposition of the given problem statement to be used during the conceptual design phase. Transform the complex task into a sequence of smaller tasks recursively until the smallest sub-tasks can be easily translated into practical details.\n"
    "Crucially, separate function from implementation. Use generic functions for each task without specifying how to implement it (e.g., use 'store data' not 'save to SQL', or 'remove material' not 'grind wood'). This enables creativity in developing high-quality concepts.\n"
    "The decomposition must be EXHAUSTIVE, highly detailed, and technical. You must generate at least 5 to 10 Level 1 (Main) Functions. Each Level 1 function must be decomposed into 3 to 5 Level 2 (Sub) Functions, and wherever technically possible, further down into Level 3 (Sub-Sub) Functions. Do not summarize or combine functions; break them down to their most atomic, fundamental operations.\n"
    "Every function must strictly use a Verb + Noun pair. The system analyzes hardware, software, or hybrid systems. For each function (root, main, sub, and sub-sub-functions), explicitly identify the separate engineering flows into and out of the function:\n"
    "1) Material Flow: physical objects or substances acted upon. (For pure software, map to structural data entities, datasets, or use 'N/A').\n"
    "2) Energy Flow: power necessary to perform operations (e.g., electrical, mechanical, human). (For pure software, map to compute execution, triggers, or use 'N/A').\n"
    "3) Information Flow: control systems, sensors, signals, data payloads, or logical states.\n"
    "Do not include physical hardware components (e.g., pump, server) or specific software technologies (e.g., React, SQL). Present the output using the required JSON schema, filling in the generic Verb+Noun function name and the associated material, energy, and information flows for every level."),
    ("human", "Problem Statement: {problem_statement}\n\nValidation Feedback (if any): {validation_feedback}\n\nPlease generate the highly detailed functional tree obeying the structured flows and Verb+Noun rules strictly.")
])

# Use structure for final output parsing
phase1_generator = generator_prompt | generator_llm.with_structured_output(FunctionalTree)

# Validator
validator_llm = ChatGroq(temperature=0.0, model_name="llama-3.1-8b-instant", groq_api_key=settings.GROQ_API_KEY, max_retries=6)

validator_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an Engineering Validator. Evaluate the functional decomposition tree. Rules to check:\n1) NO physical components, specific real-world technologies, or specific software frameworks (e.g. 'solar', 'pump', 'React', 'SQL').\n2) Functions must be generic and abstract (Verb + Noun) specifying WHAT to do, not HOW to implement it (e.g., 'remove material' not 'grind wood', 'store information' not 'save to database').\n3) There must exist a defined hierarchy (root -> main_functions -> sub_functions).\n4) Separate Material, Energy, and Information flows MUST be identified for each function. Note: for software functions, Material/Energy flows might be 'N/A' or mapped to digital analogs (like 'structured data' or 'compute triggers'); ensure this mapping is logically sound.\nIf valid, return is_valid=True and empty feedback. If invalid, return is_valid=False and specify the exact rule violations."),
    ("human", "Functional Tree JSON to validate: {functional_tree}")
])

phase1_validator = validator_prompt | validator_llm.with_structured_output(ValidationResult)
