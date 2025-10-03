"use client";

import { useEffect, useState, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import axios from "axios";
 import { LiveKitRoom, RoomAudioRenderer, useVoiceAssistant } from "@livekit/components-react";

function TutoringContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const lessonId = searchParams.get("lesson");

  const [sessionData, setSessionData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [transcript, setTranscript] = useState<{user: string[], ai: string[]}>({user: [], ai: []});

  useEffect(() => {
    if (lessonId) {
      startSession();
    }
  }, [lessonId]);

  const startSession = async () => {
    try {
      setLoading(true);
      
      // Generate token using local Next.js API endpoint (WORKING VERSION)
      const roomName = `rapidolingo_${lessonId}_${Date.now()}`;
      const identity = `student_${Math.random().toString(36).substring(7)}`;
      
      console.log("Generating token locally...");
      console.log("  Lesson:", lessonId);
      console.log("  Room:", roomName);
      console.log("  Identity:", identity);
      
      const response = await axios.post('/api/token', {
        room: roomName,
        identity: identity
      });
      
      console.log("Token generated successfully!");
      console.log("  LiveKit URL:", response.data.livekit_url);
      console.log("  Token length:", response.data.token.length);
      
      // Map lesson to agent name
      const agentNames: {[key: string]: string} = {
        restaurant: "María (Restaurant Server)",
        airport: "Carlos (Airport Agent)",
        hotel: "Sofia (Hotel Agent)",
        directions: "Miguel (Directions Guide)",
        shopping: "Ana (Shopping Assistant)",
        social_meetup: "Ana (Social Friend)",
        social_party: "Ana (Social Friend)",
        exam_prep: "Profesora López (Teacher)",
        social: "Ana (Social Friend)",
        teacher: "Profesora López (Teacher)"
      };
      
      setSessionData({
        session_id: response.data.session_id,
        livekit_token: response.data.token,
        livekit_url: response.data.livekit_url,
        agent_name: agentNames[lessonId || 'restaurant'] || "Teacher"
      });
    } catch (err: any) {
      console.error("Failed to start session:", err);
      setError(err.response?.data?.error || err.message || "Failed to start session");
    } finally {
      setLoading(false);
    }
  };

  const endSession = async () => {
    if (sessionData) {
      try {
        await axios.post(
          `${process.env.NEXT_PUBLIC_API_URL}/api/session/${sessionData.session_id}/end`
        );
      } catch (err) {
        console.error("Failed to end session:", err);
      }
    }
    router.push("/dashboard");
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-red-600 mx-auto mb-4"></div>
          <p className="text-white text-xl">Connecting to your tutor...</p>
        </div>
      </div>
    );
  }

  if (error || !sessionData) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="bg-white rounded-xl p-8 max-w-md">
          <h2 className="text-2xl font-bold text-red-600 mb-4">Connection Error</h2>
          <p className="text-gray-700 mb-6">{error || "Failed to start session"}</p>
          <button
            onClick={() => router.push("/dashboard")}
            className="w-full py-3 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 transition"
          >
            Return to Dashboard
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex">
      {/* Main session area */}
      <div className="flex-1">
        <LiveKitRoom
          token={sessionData.livekit_token}
          serverUrl={sessionData.livekit_url}
          connect={true}
          audio={true}
          video={false}
          onError={(error) => {
            console.error("LiveKit Room Error:", error);
            setError(error.message);
          }}
          onConnected={() => {
            console.log("✓ Connected to LiveKit room - audio should be active");
          }}
          className="flex flex-col items-center justify-center min-h-screen"
        >
        <div className="max-w-2xl w-full px-6">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-white mb-2">
              {sessionData?.agent_name || "Loading..."}
            </h1>
            <p className="text-gray-400">Speak naturally - your tutor is listening</p>
          </div>

          {/* Voice Visualizer */}
          <div className="bg-white bg-opacity-10 backdrop-blur-lg rounded-2xl p-12 mb-8">
            <div className="flex justify-center items-center space-x-3 mb-6">
              {[1, 2, 3, 4, 5].map((i) => (
                <div
                  key={i}
                  className="w-2 bg-red-600 rounded-full animate-pulse"
                  style={{
                    height: `${Math.random() * 60 + 20}px`,
                    animationDelay: `${i * 0.1}s`
                  }}
                />
              ))}
            </div>
            <p className="text-center text-white text-lg">
              🎤 Voice conversation active
            </p>
          </div>

          {/* Session Info */}
          <div className="bg-white bg-opacity-10 backdrop-blur-lg rounded-xl p-6 mb-6">
            <div className="grid grid-cols-2 gap-4 text-center">
              <div>
                <div className="text-gray-400 text-sm mb-1">Response Time</div>
                <div className="text-white text-2xl font-bold">&lt;100ms</div>
              </div>
              <div>
                <div className="text-gray-400 text-sm mb-1">Session Time</div>
                <div className="text-white text-2xl font-bold">0:00</div>
              </div>
            </div>
          </div>

          {/* Tips */}
          <div className="bg-white bg-opacity-5 backdrop-blur-lg rounded-xl p-6 mb-8">
            <h3 className="text-white font-semibold mb-3">💡 Tips</h3>
            <ul className="text-gray-300 text-sm space-y-2">
              <li>• Speak clearly and naturally</li>
              <li>• Ask for repetition if needed</li>
              <li>• Don't worry about mistakes - practice makes perfect!</li>
            </ul>
          </div>

          {/* End Session Button */}
          <button
            onClick={endSession}
            className="w-full py-4 bg-red-600 text-white font-semibold rounded-xl hover:bg-red-700 transition"
          >
            End Session
          </button>
        </div>

        <RoomAudioRenderer />
        <VoiceAssistantComponent />
      </LiveKitRoom>
      </div>

      {/* Transcript section */}
      <div className="w-96 bg-gray-800 p-6 overflow-y-auto">
        <h3 className="text-white text-lg font-semibold mb-4">Conversation Transcript</h3>

        <div className="space-y-4">
          {/* User's speech */}
          <div>
            <div className="text-sm text-gray-400 mb-1">You:</div>
            {transcript.user.map((text, index) => (
              <div key={index} className="text-white bg-blue-600 p-2 rounded mb-2">
                {text}
              </div>
            ))}
          </div>

          {/* AI's responses */}
          <div>
            <div className="text-sm text-gray-400 mb-1">
              {sessionData?.agent_name || "AI Tutor"}:
            </div>
            {transcript.ai.map((text, index) => (
              <div key={index} className="text-white bg-green-600 p-2 rounded mb-2">
                {text}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function VoiceAssistantComponent() {
  const { state, audioTrack } = useVoiceAssistant();

  useEffect(() => {
    console.log("Voice Assistant State:", state);
  }, [state]);

  return null;
}

export default function TutoringPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading...</div>
      </div>
    }>
      <TutoringContent />
    </Suspense>
  );
}

