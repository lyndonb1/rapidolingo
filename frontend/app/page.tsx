import Link from "next/link";
import { SignInButton, SignUpButton, SignedIn, SignedOut } from "@clerk/nextjs";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 via-white to-yellow-50">
      {/* Navigation */}
      <nav className="container mx-auto px-6 py-6 flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <span className="text-3xl font-bold text-red-600">RápidoLingo</span>
        </div>
        <div className="flex items-center space-x-4">
          <SignedOut>
            <SignInButton mode="modal">
              <button className="px-4 py-2 text-gray-700 hover:text-red-600 transition">
                Sign In
              </button>
            </SignInButton>
            <SignUpButton mode="modal">
              <button className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition">
                Get Started
              </button>
            </SignUpButton>
          </SignedOut>
          <SignedIn>
            <Link href="/dashboard">
              <button className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition">
                Dashboard
              </button>
            </Link>
          </SignedIn>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="container mx-auto px-6 py-20">
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-6xl font-bold text-gray-900 mb-6">
            Learn Spanish at
            <span className="text-red-600"> Human Speed</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Real-time AI conversations powered by Cerebras ultra-fast inference.
            Practice with specialized tutors in realistic scenarios.
          </p>
          
          <div className="flex justify-center space-x-4 mb-16">
            <SignedOut>
              <SignUpButton mode="modal">
                <button className="px-8 py-4 bg-red-600 text-white text-lg font-semibold rounded-lg hover:bg-red-700 transition shadow-lg">
                  Start Learning Free
                </button>
              </SignUpButton>
            </SignedOut>
            <SignedIn>
              <Link href="/dashboard">
                <button className="px-8 py-4 bg-red-600 text-white text-lg font-semibold rounded-lg hover:bg-red-700 transition shadow-lg">
                  Go to Dashboard
                </button>
              </Link>
            </SignedIn>
            <button className="px-8 py-4 bg-white text-gray-700 text-lg font-semibold rounded-lg hover:bg-gray-50 transition border-2 border-gray-200">
              Watch Demo
            </button>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-8 max-w-3xl mx-auto mb-20">
            <div className="text-center">
              <div className="text-4xl font-bold text-red-600 mb-2">&lt;100ms</div>
              <div className="text-gray-600">Response Time</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-red-600 mb-2">6</div>
              <div className="text-gray-600">Specialized Tutors</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-red-600 mb-2">$7.99</div>
              <div className="text-gray-600">Per Month</div>
            </div>
          </div>
        </div>

        {/* Features */}
        <div className="max-w-6xl mx-auto grid md:grid-cols-3 gap-8 mb-20">
          <div className="bg-white p-8 rounded-xl shadow-lg">
            <div className="text-4xl mb-4">⚡</div>
            <h3 className="text-2xl font-bold mb-3">Ultra-Fast AI</h3>
            <p className="text-gray-600">
              Powered by Cerebras for instant responses. Conversations feel natural and immediate.
            </p>
          </div>
          
          <div className="bg-white p-8 rounded-xl shadow-lg">
            <div className="text-4xl mb-4">🎭</div>
            <h3 className="text-2xl font-bold mb-3">Multi-Agent Scenarios</h3>
            <p className="text-gray-600">
              Practice at restaurants, airports, hotels. Each agent has unique personality and voice.
            </p>
          </div>
          
          <div className="bg-white p-8 rounded-xl shadow-lg">
            <div className="text-4xl mb-4">🗣️</div>
            <h3 className="text-2xl font-bold mb-3">Real Voice</h3>
            <p className="text-gray-600">
              Speak naturally. Get pronunciation feedback. Build confidence through conversation.
            </p>
          </div>
        </div>

        {/* CTA */}
        <div className="bg-red-600 rounded-2xl p-12 text-center text-white max-w-4xl mx-auto">
          <h2 className="text-4xl font-bold mb-4">Ready to speak Spanish fluently?</h2>
          <p className="text-xl mb-8 opacity-90">
            Join thousands learning at human speed with AI tutors
          </p>
          <SignedOut>
            <SignUpButton mode="modal">
              <button className="px-10 py-4 bg-white text-red-600 text-lg font-semibold rounded-lg hover:bg-gray-100 transition">
                Get Started - It's Free
              </button>
            </SignUpButton>
          </SignedOut>
          <SignedIn>
            <Link href="/onboarding">
              <button className="px-10 py-4 bg-white text-red-600 text-lg font-semibold rounded-lg hover:bg-gray-100 transition">
                Complete Onboarding
              </button>
            </Link>
          </SignedIn>
        </div>
      </main>

      {/* Footer */}
      <footer className="container mx-auto px-6 py-12 text-center text-gray-600">
        <p>© 2025 RápidoLingo. Built for FutureStack GenAI Hackathon.</p>
        <p className="mt-2">Powered by Cerebras, LiveKit, and Cartesia</p>
      </footer>
    </div>
  );
}

