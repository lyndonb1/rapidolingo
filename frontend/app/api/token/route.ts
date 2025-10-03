import { NextRequest, NextResponse } from 'next/server';
import { AccessToken } from 'livekit-server-sdk';

// Do not cache endpoint result
export const revalidate = 0;

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { room, identity } = body;

    if (!room) {
      return NextResponse.json(
        { error: 'Missing "room" parameter' },
        { status: 400 }
      );
    }

    if (!identity) {
      return NextResponse.json(
        { error: 'Missing "identity" parameter' },
        { status: 400 }
      );
    }

    // Get credentials from environment
    const apiKey = process.env.LIVEKIT_API_KEY || 'APIVDp9yECeVCS4';
    const apiSecret = process.env.LIVEKIT_API_SECRET || '5imN1eHgZup7LrbeTL3TYfNYZ8M6ASLDIZNFyBItlXXB';
    const wsUrl = process.env.LIVEKIT_URL || 'wss://wemakedevshackathontest-m3efiyvp.livekit.cloud';

    console.log('[Token Endpoint] Generating token...');
    console.log('  API Key:', apiKey);
    console.log('  Room:', room);
    console.log('  Identity:', identity);

    if (!apiKey || !apiSecret || !wsUrl) {
      return NextResponse.json(
        { error: 'Server misconfigured - missing LiveKit credentials' },
        { status: 500 }
      );
    }

    // Create access token
    const at = new AccessToken(apiKey, apiSecret, { identity });
    at.addGrant({
      room,
      roomJoin: true,
      canPublish: true,
      canSubscribe: true,
    });

    const token = await at.toJwt();
    
    console.log('[Token Endpoint] Token generated successfully');

    return NextResponse.json(
      { 
        token,
        livekit_url: wsUrl,
        session_id: `session_${Date.now()}`,
        agent_name: 'María (Restaurant Server)'
      },
      { 
        headers: { 
          'Cache-Control': 'no-store, no-cache, must-revalidate',
          'Pragma': 'no-cache',
          'Expires': '0'
        } 
      }
    );
  } catch (error: any) {
    console.error('[Token Endpoint] Error:', error);
    return NextResponse.json(
      { error: error.message || 'Failed to generate token' },
      { status: 500 }
    );
  }
}

