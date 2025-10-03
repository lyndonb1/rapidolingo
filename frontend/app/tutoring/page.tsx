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

  useEffect(() => {
    if (lessonId) {
      startSession();
    }
  }, [lessonId]);

  const startSession = async () => {
    try {
      setLoading(true);
      
      // Generate token using local Next.js API endpoint
      const roomName = `rapidolingo_${lessonId}_${Date.now()}`;
      const identity = `student_${Math.random().toString(36).substring(7)}`;
      
      console.log("Generating token locally...");
      console.log("  Room:", roomName);
      console.log("  Identity:", identity);
      
      const response = await axios.post('/api/token', {
        room: roomName,
        identity: identity
      });
      
      console.log("Token generated successfully!");
      console.log("  LiveKit URL:", response.data.livekit_url);
      console.log("  Token length:", response.data.token.length);
      
      setSessionData({
        session_id: response.data.session_id,
        livekit_token: response.data.token,
        livekit_url: response.data.livekit_url,
        agent_name: response.data.agent_name
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
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
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
              {sessionData.agent_name}
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

