#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime

def generate_index():
    pub_dir = os.path.dirname(os.path.abspath(__file__))
    math_dir = os.path.join(pub_dir, 'math')
    
    # CSS Template
    css_template = """
    <style>
        :root {{
            --bg-color: #0b0e14;
            --card-bg: rgba(23, 28, 38, 0.7);
            --accent-primary: #4f46e5;
            --accent-secondary: #06b6d4;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --glass-border: rgba(255, 255, 255, 0.1);
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }}
        body {{
            font-family: 'Inter', 'Outfit', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            min-height: 100vh;
            background-image: 
                radial-gradient(circle at 20% 20%, rgba(79, 70, 229, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 80% 80%, rgba(6, 182, 212, 0.15) 0%, transparent 40%);
        }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 4rem 2rem; }}
        header {{ text-align: center; margin-bottom: 5rem; }}
        h1 {{ font-family: 'Outfit', sans-serif; font-size: 3.5rem; font-weight: 800; background: linear-gradient(135deg, #fff 0%, #94a3b8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .subtitle {{ color: var(--text-muted); font-size: 1.1rem; margin-top: 0.5rem; }}
        .section {{ margin-bottom: 4rem; }}
        .section-title {{ font-family: 'Outfit', sans-serif; font-size: 1.5rem; font-weight: 600; margin-bottom: 2rem; display: flex; align-items: center; gap: 1rem; color: var(--accent-secondary); }}
        .section-title::after {{ content: ''; height: 1px; flex-grow: 1; background: linear-gradient(to right, var(--accent-secondary), transparent); }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; }}
        .card {{ background: var(--card-bg); border: 1px solid var(--glass-border); border-radius: 16px; padding: 1.5rem; text-decoration: none; color: inherit; backdrop-filter: blur(12px); display: flex; flex-direction: column; position: relative; overflow: hidden; }}
        .card:hover {{ transform: translateY(-5px); border-color: var(--accent-primary); box-shadow: 0 10px 30px rgba(0,0,0,0.3); }}
        .card-title {{ font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem; color: #fff; }}
        .card-path {{ font-family: monospace; font-size: 0.8rem; color: var(--text-muted); }}
        .card-dir {{ color: var(--accent-secondary); font-weight: 600; }}
        .footer {{ text-align: center; padding: 4rem; color: var(--text-muted); font-size: 0.8rem; }}
        .back-link {{ display: inline-flex; align-items: center; gap: 0.5rem; color: var(--accent-primary); text-decoration: none; margin-bottom: 2rem; font-weight: 500; }}
        .back-link:hover {{ text-decoration: underline; }}
    </style>
    """

    def create_card(filename, is_dir=False):
        if is_dir:
            return f"""
                <a href="{filename}/index.html" class="card">
                    <h3 class="card-title card-dir">📁 {filename.upper()}</h3>
                    <p class="card-path">Thư mục con</p>
                </a>"""
        display_name = filename.replace('-export.html', '').replace('.html', '')
        return f"""
                <a href="{filename}" class="card">
                    <h3 class="card-title">📄 {display_name}</h3>
                    <p class="card-path">{filename}</p>
                </a>"""

    html_base = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    {css}
</head>
<body>
    <div class="container">
        {header_content}
        <div class="section">
            <h2 class="section-title">{section_name}</h2>
            <div class="grid">
                {cards}
            </div>
        </div>
        <footer class="footer">
            <p>&copy; 2026 LamVIS Project. Tự động cập nhật bởi gen_index.py</p>
        </footer>
    </div>
</body>
</html>"""

    # --- 1. Generate pub/index.html ---
    pub_files = sorted([f for f in os.listdir(pub_dir) if f.endswith('.html') and f != 'index.html'])
    pub_cards = "".join([create_card(f) for f in pub_files])
    if os.path.isdir(math_dir):
        pub_cards += create_card('math', is_dir=True)
    
    header_pub = """
        <header>
            <h1>LamVIS Library</h1>
            <p class="subtitle">Danh sách các cấu hình đồ họa xuất bản</p>
        </header>"""
    
    with open(os.path.join(pub_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_base.format(
            title="LamVIS - Thư viện Đồ họa",
            css=css_template,
            header_content=header_pub,
            section_name="Thư mục Gốc",
            cards=pub_cards
        ))

    # --- 2. Generate pub/math/index.html ---
    if os.path.exists(math_dir):
        math_files = sorted([f for f in os.listdir(math_dir) if f.endswith('.html') and f != 'index.html'])
        math_cards = "".join([create_card(f) for f in math_files])
        
        header_math = """
            <a href="../index.html" class="back-link">← Quay lại Thư mục Gốc</a>
            <header>
                <h1>Math Library</h1>
                <p class="subtitle">Đồ họa toán học chuyên sâu</p>
            </header>"""
        
        with open(os.path.join(math_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html_base.format(
                title="LamVIS - Math Library",
                css=css_template,
                header_content=header_math,
                section_name="Cấu hình Toán học",
                cards=math_cards
            ))
    
    print("Đã tạo thành công 2 file index.html riêng biệt!")

    # --- 3. Git Operations ---
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Update index.html - {now}"
        
        print(f"Đang thực hiện Git commit: {commit_message}...")
        
        # Thêm tất cả thay đổi
        subprocess.run(["git", "add", "."], cwd=pub_dir, check=True)
        
        # Commit với message thời gian
        subprocess.run(["git", "commit", "-m", commit_message], cwd=pub_dir, check=True)
        
        # Push lên remote
        print("Đang Push lên remote...")
        subprocess.run(["git", "push"], cwd=pub_dir, check=True)
        
        print("✅ Đã hoàn tất: Index generated and pushed to Git!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi Git: {e}")
    except Exception as e:
        print(f"❌ Có lỗi xảy ra: {e}")

if __name__ == "__main__":
    generate_index()
