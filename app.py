
from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/api/get_video_info', methods=['POST'])
def get_video_info():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'forcejson': True,
        'extract_flat': False,
        'format': 'best',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = [
                {
                    'format_id': f['format_id'],
                    'ext': f['ext'],
                    'resolution': f.get('height', 'N/A'),
                    'filesize': f.get('filesize', 0),
                    'url': f['url']
                }
                for f in info['formats'] if f.get('height') and f.get('url')
            ]
            return jsonify({
                'title': info.get('title', 'No Title'),
                'thumbnail': info.get('thumbnail'),
                'formats': formats
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
