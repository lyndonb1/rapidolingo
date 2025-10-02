"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useUser } from "@clerk/nextjs";

export default function Onboarding() {
  const router = useRouter();
  const { user } = useUser();
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    name: user?.firstName || "",
    level: "",
    goal: ""
  });

  const handleNext = () => {
    if (step === 1 && formData.name) {
      setStep(2);
    } else if (step === 2 && formData.level) {
      setStep(3);
    }
  };

  const handleComplete = () => {
    // Save to localStorage for MVP
    localStorage.setItem("rapidolingo_profile", JSON.stringify(formData));
    router.push("/dashboard");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 to-yellow-50 flex items-center justify-center p-6">
      <div className="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full">
        {/* Progress */}
        <div className="flex justify-between mb-8">
          {[1, 2, 3].map((s) => (
            <div
              key={s}
              className={`h-2 flex-1 mx-1 rounded-full ${
                s <= step ? "bg-red-600" : "bg-gray-200"
              }`}
            />
          ))}
        </div>

        {/* Step 1: Name */}
        {step === 1 && (
          <div>
            <h2 className="text-3xl font-bold text-gray-900 mb-2">Welcome!</h2>
            <p className="text-gray-600 mb-6">What should we call you?</p>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              placeholder="Your name"
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-red-600 focus:outline-none mb-6"
            />
            <button
              onClick={handleNext}
              disabled={!formData.name}
              className="w-full py-3 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Continue
            </button>
          </div>
        )}

        {/* Step 2: Level */}
        {step === 2 && (
          <div>
            <h2 className="text-3xl font-bold text-gray-900 mb-2">Your Spanish Level</h2>
            <p className="text-gray-600 mb-6">This helps us personalize your experience</p>
            <div className="space-y-3 mb-6">
              {[
                { value: "beginner", label: "Beginner", desc: "Just starting out" },
                { value: "intermediate", label: "Intermediate", desc: "Can have basic conversations" },
                { value: "advanced", label: "Advanced", desc: "Fluent, need practice" }
              ].map((level) => (
                <button
                  key={level.value}
                  onClick={() => setFormData({...formData, level: level.value})}
                  className={`w-full p-4 border-2 rounded-lg text-left transition ${
                    formData.level === level.value
                      ? "border-red-600 bg-red-50"
                      : "border-gray-200 hover:border-gray-300"
                  }`}
                >
                  <div className="font-semibold text-gray-900">{level.label}</div>
                  <div className="text-sm text-gray-600">{level.desc}</div>
                </button>
              ))}
            </div>
            <button
              onClick={handleNext}
              disabled={!formData.level}
              className="w-full py-3 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 transition disabled:opacity-50"
            >
              Continue
            </button>
          </div>
        )}

        {/* Step 3: Goal */}
        {step === 3 && (
          <div>
            <h2 className="text-3xl font-bold text-gray-900 mb-2">Learning Goal</h2>
            <p className="text-gray-600 mb-6">What's your main reason for learning?</p>
            <div className="space-y-3 mb-6">
              {[
                { value: "travel", label: "Travel", desc: "Navigate Spanish-speaking countries" },
                { value: "exams", label: "Exams", desc: "Prepare for tests" },
                { value: "social", label: "Social", desc: "Connect with Spanish speakers" }
              ].map((goal) => (
                <button
                  key={goal.value}
                  onClick={() => setFormData({...formData, goal: goal.value})}
                  className={`w-full p-4 border-2 rounded-lg text-left transition ${
                    formData.goal === goal.value
                      ? "border-red-600 bg-red-50"
                      : "border-gray-200 hover:border-gray-300"
                  }`}
                >
                  <div className="font-semibold text-gray-900">{goal.label}</div>
                  <div className="text-sm text-gray-600">{goal.desc}</div>
                </button>
              ))}
            </div>
            <button
              onClick={handleComplete}
              disabled={!formData.goal}
              className="w-full py-3 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 transition disabled:opacity-50"
            >
              Complete Setup
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

