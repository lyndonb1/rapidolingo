"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useUser, UserButton } from "@clerk/nextjs";
import axios from "axios";

interface Lesson {
  id: string;
  title: string;
  description: string;
  difficulty: string;
  agent_type: string;
  category: string;
}

export default function Dashboard() {
  const router = useRouter();
  const { user } = useUser();
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState<any>(null);

  useEffect(() => {
    // Load profile from localStorage
    const savedProfile = localStorage.getItem("rapidolingo_profile");
    if (savedProfile) {
      setProfile(JSON.parse(savedProfile));
    } else {
      // Redirect to onboarding if no profile
      router.push("/onboarding");
      return;
    }

    // Fetch lessons from backend
    fetchLessons();
  }, []);

  const fetchLessons = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const response = await axios.get(
        `${apiUrl}/api/lessons`
      );
      setLessons(response.data);
    } catch (error) {
      console.error("Failed to fetch lessons:", error);
    } finally {
      setLoading(false);
    }
  };

  const startLesson = async (lessonId: string) => {
    router.push(`/tutoring?lesson=${lessonId}`);
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case "beginner":
        return "bg-green-100 text-green-800";
      case "intermediate":
        return "bg-yellow-100 text-yellow-800";
      case "advanced":
        return "bg-red-100 text-red-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case "travel":
        return "✈️";
      case "daily_life":
        return "🏪";
      case "social":
        return "👥";
      case "academic":
        return "📚";
      default:
        return "📝";
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl text-gray-600">Loading lessons...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <span className="text-2xl font-bold text-red-600">RápidoLingo</span>
            <span className="text-gray-400">|</span>
            <span className="text-gray-700">Dashboard</span>
          </div>
          <div className="flex items-center space-x-4">
            <div className="text-right mr-4">
              <div className="text-sm font-semibold text-gray-900">
                {profile?.name || user?.firstName}
              </div>
              <div className="text-xs text-gray-500 capitalize">{profile?.level}</div>
            </div>
            <UserButton />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        {/* Welcome Section */}
        <div className="bg-gradient-to-r from-red-600 to-red-500 rounded-2xl p-8 mb-8 text-white">
          <h1 className="text-3xl font-bold mb-2">
            ¡Hola, {profile?.name || user?.firstName}!
          </h1>
          <p className="text-red-100">
            Ready to practice your Spanish? Choose a scenario below to start a conversation.
          </p>
        </div>

        {/* Lessons Grid */}
        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Available Lessons</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {lessons.map((lesson) => {
              const isEnabled = lesson.id === "restaurant";
              return (
                <div
                  key={lesson.id}
                  className={`bg-white rounded-xl shadow-sm border p-6 transition ${
                    isEnabled
                      ? "border-gray-200 hover:shadow-lg"
                      : "border-gray-100 opacity-50 cursor-not-allowed"
                  }`}
                >
                  <div className="flex justify-between items-start mb-3">
                    <span className="text-3xl">{getCategoryIcon(lesson.category)}</span>
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-semibold ${getDifficultyColor(
                        lesson.difficulty
                      )}`}
                    >
                      {lesson.difficulty}
                    </span>
                  </div>
                  <h3 className={`text-xl font-bold mb-2 ${isEnabled ? "text-gray-900" : "text-gray-400"}`}>
                    {lesson.title}
                  </h3>
                  <p className={`text-sm mb-4 ${isEnabled ? "text-gray-600" : "text-gray-400"}`}>
                    {lesson.description}
                  </p>
                  <button
                    onClick={() => isEnabled && startLesson(lesson.id)}
                    disabled={!isEnabled}
                    className={`w-full py-3 font-semibold rounded-lg transition ${
                      isEnabled
                        ? "bg-red-600 text-white hover:bg-red-700"
                        : "bg-gray-200 text-gray-400 cursor-not-allowed"
                    }`}
                  >
                    {isEnabled ? "Start Lesson" : "Coming Soon"}
                  </button>
                </div>
              );
            })}
          </div>
        </div>

        {/* Quick Stats */}
        <div className="mt-8 grid md:grid-cols-3 gap-6">
          <div className="bg-white rounded-xl p-6 border border-gray-200">
            <div className="text-3xl mb-2">🎯</div>
            <div className="text-2xl font-bold text-gray-900 mb-1">0</div>
            <div className="text-sm text-gray-600">Lessons Completed</div>
          </div>
          <div className="bg-white rounded-xl p-6 border border-gray-200">
            <div className="text-3xl mb-2">⚡</div>
            <div className="text-2xl font-bold text-gray-900 mb-1">0</div>
            <div className="text-sm text-gray-600">Minutes Practiced</div>
          </div>
          <div className="bg-white rounded-xl p-6 border border-gray-200">
            <div className="text-3xl mb-2">🔥</div>
            <div className="text-2xl font-bold text-gray-900 mb-1">0</div>
            <div className="text-sm text-gray-600">Day Streak</div>
          </div>
        </div>
      </main>
    </div>
  );
}

