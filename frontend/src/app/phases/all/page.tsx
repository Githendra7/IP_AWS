import { Suspense } from "react";
import { PhasesContent } from "./PhasesContent";
import { motion } from "framer-motion";

export const dynamic = "force-dynamic";

export default async function AllPhasesPage({
  searchParams,
}: {
  searchParams: Promise<{ projectId?: string }>;
}) {
  const { projectId } = await searchParams;

  return (
    <Suspense
      fallback={
        <div className="flex items-center justify-center h-screen bg-[#FDFCFB]">
          <div className="flex flex-col items-center">
            <div className="relative w-16 h-16 mb-6">
              <div className="absolute inset-0 border-4 border-zinc-100 rounded-full" />
              <div className="absolute inset-0 border-4 border-zinc-900 rounded-full border-t-transparent animate-spin" />
            </div>
            <span className="text-sm font-bold text-zinc-400 tracking-[0.2em] uppercase text-center ml-2">
              Assembling Dashboard...
            </span>
          </div>
        </div>
      }
    >
      <PhasesContent projectId={projectId || null} />
    </Suspense>
  );
}