"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Mail, ArrowRight, AlertCircle, CheckCircle2 } from "lucide-react";
import { motion } from "motion/react";
import { forgotPassword } from "@/lib/api";

export default function ForgotPasswordPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess(false);
    
    try {
      await forgotPassword(email);
      setSuccess(true);
    } catch (err: any) {
      setError(err.message || "Failed to send reset link");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen lg:grid lg:grid-cols-2 bg-background font-sans">
      {/* Left side: Visuals */}
      <div className="hidden lg:flex flex-col justify-between p-12 bg-zinc-900 text-white relative overflow-hidden">
        <div className="relative z-10">
          <div className="flex items-center gap-2 mb-8">
             <div className="bg-white rounded-lg p-2">
                <div className="h-6 w-6 border-2 border-zinc-900 rounded-sm"></div>
             </div>
             <span className="text-2xl font-bold tracking-tight">ProtoStruc</span>
          </div>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-5xl font-bold mb-6 leading-tight">
              Regain access to your workflows.
            </h1>
            <p className="text-zinc-400 text-xl max-w-md">
              Enter your email and we'll send you a secure link to reset your password and get back to building.
            </p>
          </motion.div>
        </div>
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-to-br from-zinc-800/20 to-transparent rounded-full blur-3xl -z-0"></div>
      </div>

      {/* Right side: Form */}
      <div className="flex-1 flex items-center justify-center p-8 bg-[#FDFCFB]">
        <motion.div 
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="w-full max-w-[400px]"
        >
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-zinc-900 mb-2">Forgot Password</h2>
            <p className="text-zinc-500 font-medium">Enter your email to receive a reset link.</p>
          </div>

          {success ? (
            <motion.div 
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="space-y-6"
            >
              <div className="bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl p-6 flex flex-col items-center text-center gap-4">
                <div className="h-12 w-12 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-600">
                  <CheckCircle2 className="h-6 w-6" />
                </div>
                <div>
                  <h3 className="font-bold text-lg mb-1">Check your email</h3>
                  <p className="text-sm">We've sent a password reset link to <span className="font-bold">{email}</span></p>
                </div>
              </div>
              <Link href="/login">
                <Button variant="outline" className="w-full h-12 rounded-xl font-bold">Back to login</Button>
              </Link>
            </motion.div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-5">
              {error && (
                <motion.div 
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-red-50 border border-red-200 text-red-600 rounded-xl p-4 flex items-start gap-3 text-sm font-medium"
                >
                  <AlertCircle className="h-5 w-5 shrink-0" />
                  {error}
                </motion.div>
              )}

              <div className="space-y-2">
                <Label htmlFor="email" className="text-zinc-700 font-bold">Email Address</Label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-zinc-400" />
                  <Input
                    id="email"
                    type="email"
                    placeholder="you@company.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    className="pl-10 h-12 border-zinc-200 focus:border-zinc-900 transition-all rounded-xl"
                  />
                </div>
              </div>

              <Button 
                type="submit" 
                className="w-full h-12 rounded-xl bg-zinc-900 hover:bg-zinc-800 text-white font-bold transition-all shadow-lg active:scale-[0.98] group mt-4" 
                disabled={loading}
              >
                {loading ? "Sending link..." : "Send Reset Link"}
              </Button>
              
              <p className="mt-6 text-center text-zinc-500 font-medium">
                Remember your password?{" "}
                <Link href="/login" className="text-zinc-900 font-bold hover:underline">
                  Sign in
                </Link>
              </p>
            </form>
          )}
        </motion.div>
      </div>
    </div>
  );
}
