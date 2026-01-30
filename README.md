# Music Chord Maker

A simple web-based tool that generates chord sheets for songs using AI via AI-builders-coach API.

## Features

- Clean, modern web interface
- Generate chord sheets with lyrics for any song
- Chords aligned above the correct syllables (monospace format)
- Copy button to easily paste into documents
- Uses DeepSeek AI model

## Setup

1. Install dependencies:
```bash
cd music-chord-maker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Get your AI_BUILDER_TOKEN:
   - The token is available through the AI-builders-coach MCP
   - Or check your environment variables if already set

3. Set your AI_BUILDER_TOKEN:

   **Option A: Create a `.env` file** (recommended):
   ```bash
   echo "AI_BUILDER_TOKEN=your_token_here" > .env
   ```

   **Option B: Export as environment variable**:
   ```bash
   export AI_BUILDER_TOKEN=your_token_here
   ```

4. Run the application:

   **Easy way** (uses start.sh script):
   ```bash
   ./start.sh
   ```

   **Manual way**:
   ```bash
   source venv/bin/activate
   python app.py
   ```

5. Open your browser and navigate to:
```
http://localhost:8000
```

## Usage

1. Enter a song name (e.g., "Let It Be")
2. Enter the artist (e.g., "The Beatles")
3. Click "Generate" button
4. The chord sheet will appear with chords aligned above lyrics
5. Click "Copy" to copy to clipboard

## API Endpoint

You can also use the API directly:

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"song": "Let It Be", "artist": "The Beatles"}'
```
