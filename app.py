from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Music Chord Maker")

def get_client():
    api_token = os.getenv("AI_BUILDER_TOKEN")
    if not api_token:
        raise ValueError("AI_BUILDER_TOKEN environment variable is not set.")
    return OpenAI(
        base_url="https://space.ai-builders.com/backend/v1",
        api_key=api_token
    )

SYSTEM_PROMPT = """Output a chord sheet. No introductions, no explanations, no preamble.

YOUR RESPONSE MUST START WITH "Key:" - nothing before it.

FORMAT:
Key: X

[Verse 1]
(chords above lyrics)

[Chorus]
(chords above lyrics)

RULES:
- First line MUST be "Key: X" (e.g., Key: C major)
- Chords appear DIRECTLY above the syllable they should be played on
- Use spaces to align chords precisely
- Use standard chord notation (C, Am, F, G7, Dm, etc.)
- Include section labels [Verse 1], [Chorus], [Bridge], etc."""

class ChordRequest(BaseModel):
    song: str
    artist: str

@app.get("/health")
async def health_check():
    token_set = bool(os.getenv("AI_BUILDER_TOKEN"))
    return {
        "status": "healthy",
        "token_configured": token_set
    }

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Music Chord Maker</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 900px;
                margin: 0 auto;
                background: #0f0f23;
                border-radius: 16px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
                overflow: hidden;
            }
            .header {
                background: linear-gradient(135deg, #e94560 0%, #ff6b6b 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }
            .header h1 {
                font-size: 2.2em;
                margin-bottom: 8px;
            }
            .header p {
                opacity: 0.9;
            }
            .content {
                padding: 40px;
            }
            .input-section {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-bottom: 25px;
            }
            @media (max-width: 600px) {
                .input-section {
                    grid-template-columns: 1fr;
                }
            }
            .input-group {
                display: flex;
                flex-direction: column;
            }
            .input-group label {
                color: #ccc;
                margin-bottom: 8px;
                font-weight: 500;
            }
            .input-group input {
                padding: 14px 18px;
                border: 2px solid #333;
                border-radius: 8px;
                font-size: 16px;
                background: #1a1a2e;
                color: white;
                transition: border-color 0.3s;
            }
            .input-group input:focus {
                outline: none;
                border-color: #e94560;
            }
            .input-group input::placeholder {
                color: #666;
            }
            .output-section {
                margin-bottom: 25px;
            }
            .output-section label {
                color: #ccc;
                margin-bottom: 8px;
                display: block;
                font-weight: 500;
            }
            #output {
                width: 100%;
                min-height: 450px;
                padding: 20px;
                border: 2px solid #333;
                border-radius: 8px;
                font-family: 'Courier New', Courier, monospace;
                font-size: 14px;
                background: #1a1a2e;
                color: #00ff88;
                resize: vertical;
                line-height: 1.5;
                white-space: pre;
            }
            #output:focus {
                outline: none;
                border-color: #e94560;
            }
            .button-container {
                display: flex;
                gap: 15px;
                justify-content: center;
                flex-wrap: wrap;
            }
            button {
                padding: 14px 35px;
                font-size: 1em;
                font-weight: 600;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.3s;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            #generate-btn {
                background: linear-gradient(135deg, #e94560 0%, #ff6b6b 100%);
                color: white;
            }
            #generate-btn:hover:not(:disabled) {
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(233, 69, 96, 0.4);
            }
            #generate-btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
            }
            #copy-btn {
                background: #333;
                color: white;
            }
            #copy-btn:hover {
                background: #444;
                transform: translateY(-2px);
            }
            #clear-btn {
                background: #222;
                color: #888;
            }
            #clear-btn:hover {
                background: #333;
                color: white;
                transform: translateY(-2px);
            }
            .loading {
                display: none;
                text-align: center;
                padding: 20px;
                color: #e94560;
                font-weight: 600;
            }
            .loading.show {
                display: block;
            }
            .spinner {
                border: 3px solid #333;
                border-top: 3px solid #e94560;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 10px;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .toast {
                position: fixed;
                bottom: 30px;
                left: 50%;
                transform: translateX(-50%) translateY(100px);
                background: #00ff88;
                color: #0f0f23;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: 600;
                opacity: 0;
                transition: all 0.3s;
            }
            .toast.show {
                transform: translateX(-50%) translateY(0);
                opacity: 1;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Music Chord Maker</h1>
                <p>Generate chord sheets for your favorite songs</p>
            </div>
            <div class="content">
                <div class="input-section">
                    <div class="input-group">
                        <label for="song">Song Name</label>
                        <input type="text" id="song" placeholder="e.g. Let It Be">
                    </div>
                    <div class="input-group">
                        <label for="artist">Artist</label>
                        <input type="text" id="artist" placeholder="e.g. The Beatles">
                    </div>
                </div>
                <div class="output-section">
                    <label for="output">Chord Sheet</label>
                    <textarea id="output" placeholder="Your chord sheet will appear here..." readonly></textarea>
                </div>
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    Generating chord sheet...
                </div>
                <div class="button-container">
                    <button id="generate-btn" onclick="generateChords()">Generate</button>
                    <button id="copy-btn" onclick="copyToClipboard()">Copy</button>
                    <button id="clear-btn" onclick="clearAll()">Clear</button>
                </div>
            </div>
        </div>
        <div class="toast" id="toast">Copied to clipboard!</div>
        <script>
            async function generateChords() {
                const song = document.getElementById('song').value.trim();
                const artist = document.getElementById('artist').value.trim();
                const output = document.getElementById('output');
                const generateBtn = document.getElementById('generate-btn');
                const loading = document.getElementById('loading');

                if (!song || !artist) {
                    alert('Please enter both song name and artist.');
                    return;
                }

                generateBtn.disabled = true;
                loading.classList.add('show');
                output.value = '';

                try {
                    const response = await fetch('/generate', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ song, artist })
                    });

                    if (!response.ok) {
                        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
                        throw new Error(errorData.detail || `HTTP ${response.status}`);
                    }

                    const data = await response.json();
                    output.value = data.chord_sheet;
                } catch (error) {
                    output.value = 'Error: ' + error.message;
                } finally {
                    generateBtn.disabled = false;
                    loading.classList.remove('show');
                }
            }

            function copyToClipboard() {
                const output = document.getElementById('output');
                const toast = document.getElementById('toast');

                if (!output.value) {
                    return;
                }

                navigator.clipboard.writeText(output.value).then(() => {
                    toast.classList.add('show');
                    setTimeout(() => toast.classList.remove('show'), 2000);
                });
            }

            function clearAll() {
                document.getElementById('song').value = '';
                document.getElementById('artist').value = '';
                document.getElementById('output').value = '';
            }

            // Enter key triggers generate
            document.getElementById('song').addEventListener('keydown', function(e) {
                if (e.key === 'Enter') generateChords();
            });
            document.getElementById('artist').addEventListener('keydown', function(e) {
                if (e.key === 'Enter') generateChords();
            });
        </script>
    </body>
    </html>
    """

@app.post("/generate")
async def generate_chords(request: ChordRequest):
    try:
        client = get_client()
        print(f"\n{'='*60}")
        print(f"REQUEST: '{request.song}' by {request.artist}")
        print(f"{'='*60}")

        response = client.chat.completions.create(
            model="deepseek",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Generate a chord sheet for \"{request.song}\" by {request.artist}"}
            ],
            temperature=1.0,
            max_tokens=4096
        )

        print(f"\nAPI RESPONSE:")
        print(f"  Model: {response.model}")
        print(f"  Usage: {response.usage.prompt_tokens} prompt + {response.usage.completion_tokens} completion = {response.usage.total_tokens} total tokens")
        print(f"  Finish reason: {response.choices[0].finish_reason if response.choices else 'N/A'}")

        if not response.choices:
            raise ValueError("No response from API")

        chord_sheet = response.choices[0].message.content.strip()

        # Strip any preamble before "Key:"
        if "Key:" in chord_sheet:
            chord_sheet = chord_sheet[chord_sheet.index("Key:"):]

        # Add song title header
        chord_sheet = f"{request.song} - {request.artist}\n\n{chord_sheet}"

        # Debug: print raw content
        raw_content = response.choices[0].message.content
        print(f"\nRAW CONTENT TYPE: {type(raw_content)}")
        print(f"RAW CONTENT LENGTH: {len(raw_content) if raw_content else 'None'}")
        print(f"RAW CONTENT REPR: {repr(raw_content[:500]) if raw_content else 'None'}...")

        print(f"\nCHORD SHEET OUTPUT:")
        print(f"{'-'*60}")
        print(chord_sheet)
        print(f"{'-'*60}\n")

        return {"chord_sheet": chord_sheet}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
