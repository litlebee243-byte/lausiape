# ==========================================
# PROJECT: NEXUS CYBER UTILITY SUITE 
# FILE: app.py
# VERSION: CYBER v6.0 - FIXED
# ==========================================

import os
import re
import json
import string
import random
import hashlib
import qrcode
from io import BytesIO
import base64
import datetime
import time
from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'nexus-cyber-secret-key-2024'

# ==========================================
# DATA STORE
# ==========================================
data_store = {
    'ucapan': [],
    'pesan': [],
    'kuis': [],
    'qr': [],
    'keuangan': [],
    'favorit': [],
    'hitung': [],
    'teks': [],
    'ketik': [],
    'konversi': []
}

# ==========================================
# FUNGSI BANTUAN
# ==========================================
def generate_qr(text):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def stylize_text(text, style='esthetic'):
    if style == 'esthetic':
        mapping = {
            'a': '𝓪', 'b': '𝓫', 'c': '𝓬', 'd': '𝓭', 'e': '𝓮',
            'f': '𝓯', 'g': '𝓰', 'h': '𝓱', 'i': '𝓲', 'j': '𝓳',
            'k': '𝓴', 'l': '𝓵', 'm': '𝓶', 'n': '𝓷', 'o': '𝓸',
            'p': '𝓹', 'q': '𝓺', 'r': '𝓻', 's': '𝓼', 't': '𝓽',
            'u': '𝓾', 'v': '𝓿', 'w': '𝔀', 'x': '𝔁', 'y': '𝔂', 'z': '𝔃'
        }
        return ''.join(mapping.get(c.lower(), c) for c in text)
    elif style == 'upside':
        mapping = {
            'a': 'ɐ', 'b': 'q', 'c': 'ɔ', 'd': 'p', 'e': 'ǝ',
            'f': 'ɟ', 'g': 'ƃ', 'h': 'ɥ', 'i': 'ᴉ', 'j': 'ɾ',
            'k': 'ʞ', 'l': 'l', 'm': 'ɯ', 'n': 'u', 'o': 'o',
            'p': 'd', 'q': 'b', 'r': 'ɹ', 's': 's', 't': 'ʇ',
            'u': 'n', 'v': 'ʌ', 'w': 'ʍ', 'x': 'x', 'y': 'ʎ', 'z': 'z'
        }
        return ''.join(mapping.get(c.lower(), c) for c in text[::-1])
    return text

# ==========================================
# HOME PAGE (MENU UTAMA)
# ==========================================
HOME_PAGE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXUS • Cyber Utility Suite</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
        
        * { 
            font-family: 'Rajdhani', sans-serif;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background: #05050a;
            min-height: 100vh;
            color: #00ffff;
            overflow-x: hidden;
        }
        
        /* ===== CYBER BACKGROUND ===== */
        .cyber-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            background: 
                radial-gradient(circle at 20% 30%, rgba(0, 255, 255, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 80% 70%, rgba(255, 0, 255, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 50% 50%, rgba(0, 100, 255, 0.05) 0%, transparent 70%);
            animation: cyberPulse 6s ease-in-out infinite alternate;
        }
        
        @keyframes cyberPulse {
            0% { opacity: 0.6; transform: scale(1); }
            100% { opacity: 1; transform: scale(1.05); }
        }
        
        .cyber-grid {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            background-image: 
                linear-gradient(rgba(0, 255, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 255, 0.03) 1px, transparent 1px);
            background-size: 50px 50px;
            animation: gridMove 15s linear infinite;
        }
        
        @keyframes gridMove {
            0% { transform: translate(0, 0); }
            100% { transform: translate(50px, 50px); }
        }
        
        .scanline {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            background: repeating-linear-gradient(
                0deg,
                transparent,
                transparent 2px,
                rgba(0, 255, 255, 0.02) 2px,
                rgba(0, 255, 255, 0.02) 4px
            );
            pointer-events: none;
            animation: scanMove 8s linear infinite;
        }
        
        @keyframes scanMove {
            0% { transform: translateY(0); }
            100% { transform: translateY(100%); }
        }
        
        /* ===== GLASS CYBER ===== */
        .glass-cyber {
            background: rgba(0, 20, 30, 0.6);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(0, 255, 255, 0.15);
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.05), inset 0 0 30px rgba(0, 255, 255, 0.02);
            position: relative;
            z-index: 1;
        }
        
        .glass-cyber::before {
            content: '';
            position: absolute;
            top: -1px;
            left: 20%;
            right: 20%;
            height: 1px;
            background: linear-gradient(90deg, transparent, #00ffff, transparent);
            animation: neonLine 3s ease-in-out infinite;
        }
        
        @keyframes neonLine {
            0%, 100% { opacity: 0.2; transform: scaleX(0.8); }
            50% { opacity: 1; transform: scaleX(1); }
        }
        
        .cyber-text {
            background: linear-gradient(135deg, #00ffff 0%, #ff00ff 50%, #00ffff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            filter: drop-shadow(0 0 20px rgba(0, 255, 255, 0.3));
        }
        
        /* ===== MENU ===== */
        .menu-cyber {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 10px;
            padding: 8px;
        }
        
        @media (max-width: 640px) {
            .menu-cyber {
                grid-template-columns: repeat(4, 1fr);
                gap: 8px;
            }
        }
        
        @media (max-width: 400px) {
            .menu-cyber {
                grid-template-columns: repeat(3, 1fr);
                gap: 6px;
            }
        }
        
        .menu-item-cyber {
            background: rgba(0, 20, 30, 0.3);
            border: 1px solid rgba(0, 255, 255, 0.08);
            border-radius: 12px;
            padding: 16px 8px;
            text-align: center;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            text-decoration: none;
            color: rgba(0, 255, 255, 0.6);
            position: relative;
            overflow: hidden;
            cursor: pointer;
            display: block;
        }
        
        .menu-item-cyber::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(0, 255, 255, 0.1), transparent 70%);
            opacity: 0;
            transition: opacity 0.5s ease;
            transform: scale(0);
        }
        
        .menu-item-cyber:hover::before {
            opacity: 1;
            transform: scale(1);
        }
        
        .menu-item-cyber:hover {
            transform: translateY(-6px) scale(1.05);
            border-color: rgba(0, 255, 255, 0.4);
            background: rgba(0, 255, 255, 0.08);
            box-shadow: 0 0 40px rgba(0, 255, 255, 0.1), inset 0 0 40px rgba(0, 255, 255, 0.05);
            color: #00ffff;
        }
        
        .menu-item-cyber:active {
            transform: scale(0.95);
        }
        
        .menu-icon-cyber {
            font-size: 2rem;
            display: block;
            margin-bottom: 4px;
            transition: transform 0.3s ease;
        }
        
        .menu-item-cyber:hover .menu-icon-cyber {
            transform: scale(1.2) rotate(-5deg);
        }
        
        .menu-label-cyber {
            font-size: 0.65rem;
            font-weight: 600;
            letter-spacing: 1px;
            text-transform: uppercase;
            font-family: 'Orbitron', sans-serif;
            display: block;
        }
        
        @media (max-width: 640px) {
            .menu-icon-cyber { font-size: 1.5rem; }
            .menu-label-cyber { font-size: 0.55rem; }
            .menu-item-cyber { padding: 12px 4px; }
        }
        
        /* ===== TITLE ===== */
        .cyber-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 4rem;
            font-weight: 900;
            background: linear-gradient(135deg, #00ffff 0%, #ff00ff 50%, #00ffff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            filter: drop-shadow(0 0 40px rgba(0, 255, 255, 0.3));
            letter-spacing: 8px;
            animation: titleGlow 3s ease-in-out infinite;
        }
        
        @keyframes titleGlow {
            0%, 100% { filter: drop-shadow(0 0 40px rgba(0, 255, 255, 0.3)); }
            50% { filter: drop-shadow(0 0 80px rgba(0, 255, 255, 0.6)); }
        }
        
        @media (max-width: 640px) {
            .cyber-title { font-size: 2.5rem; letter-spacing: 4px; }
        }
        
        .cyber-sub {
            color: rgba(0, 255, 255, 0.4);
            font-family: 'Orbitron', sans-serif;
            letter-spacing: 4px;
            font-size: 0.8rem;
            animation: subPulse 2s ease-in-out infinite;
        }
        
        @keyframes subPulse {
            0%, 100% { opacity: 0.4; }
            50% { opacity: 1; }
        }
        
        /* ===== ANIMATIONS ===== */
        .fade-cyber {
            animation: fadeCyber 0.8s ease forwards;
        }
        
        @keyframes fadeCyber {
            from { opacity: 0; transform: translateY(30px) scale(0.95); filter: blur(10px); }
            to { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
        }
        
        .float-cyber {
            animation: floatCyber 4s ease-in-out infinite;
        }
        
        @keyframes floatCyber {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        .glitch-text {
            animation: glitchText 3s infinite;
        }
        
        @keyframes glitchText {
            2%, 64% { transform: translate(2px, 0) skew(0deg); }
            4%, 60% { transform: translate(-2px, 0) skew(0deg); }
            62% { transform: translate(0, 0) skew(5deg); }
        }
        
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: rgba(0,255,255,0.02); }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #00ffff, #0088ff);
            border-radius: 10px;
        }
        
        /* Particle effect */
        .particle {
            position: fixed;
            width: 2px;
            height: 2px;
            background: #00ffff;
            border-radius: 50%;
            pointer-events: none;
            z-index: 0;
            animation: particleFloat linear infinite;
        }
        
        @keyframes particleFloat {
            0% { transform: translateY(100vh) scale(0); opacity: 0; }
            10% { opacity: 1; }
            90% { opacity: 1; }
            100% { transform: translateY(-10vh) scale(1); opacity: 0; }
        }
    </style>
</head>
<body>
    <!-- CYBER BACKGROUND -->
    <div class="cyber-bg"></div>
    <div class="cyber-grid"></div>
    <div class="scanline"></div>
    
    <!-- PARTICLES -->
    <div id="particles"></div>

    <div class="relative z-10 p-4 md:p-6 min-h-screen flex items-center justify-center">
        <div class="max-w-4xl w-full">
            <header class="text-center py-8 fade-cyber">
                <div class="float-cyber">
                    <div class="text-6xl mb-2 glitch-text">⚡</div>
                    <h1 class="cyber-title">NEXUS</h1>
                </div>
                <p class="cyber-sub mt-2">CYBER UTILITY SUITE</p>
                <p class="text-sm mt-4" style="color: rgba(0,255,255,0.3); font-family: 'Orbitron', sans-serif; letter-spacing: 2px;">
                    <span class="inline-block animate-pulse">●</span> SYSTEM ONLINE <span class="inline-block animate-pulse">●</span>
                </p>
            </header>

            <nav class="glass-cyber rounded-2xl p-6 md:p-8 fade-cyber" style="animation-delay: 0.3s;">
                <div class="menu-cyber">
                    <a href="/ucapan" class="menu-item-cyber">
                        <span class="menu-icon-cyber">🎉</span>
                        <span class="menu-label-cyber">Ucapan</span>
                    </a>
                    <a href="/pesan" class="menu-item-cyber">
                        <span class="menu-icon-cyber">💌</span>
                        <span class="menu-label-cyber">Pesan</span>
                    </a>
                    <a href="/kuis" class="menu-item-cyber">
                        <span class="menu-icon-cyber">🧠</span>
                        <span class="menu-label-cyber">Kuis</span>
                    </a>
                    <a href="/qr" class="menu-item-cyber">
                        <span class="menu-icon-cyber">📱</span>
                        <span class="menu-label-cyber">QR</span>
                    </a>
                    <a href="/keuangan" class="menu-item-cyber">
                        <span class="menu-icon-cyber">💰</span>
                        <span class="menu-label-cyber">Keuangan</span>
                    </a>
                    <a href="/hitung" class="menu-item-cyber">
                        <span class="menu-icon-cyber">⏳</span>
                        <span class="menu-label-cyber">Hitung</span>
                    </a>
                    <a href="/teks" class="menu-item-cyber">
                        <span class="menu-icon-cyber">✨</span>
                        <span class="menu-label-cyber">Teks</span>
                    </a>
                    <a href="/favorit" class="menu-item-cyber">
                        <span class="menu-icon-cyber">⭐</span>
                        <span class="menu-label-cyber">Favorit</span>
                    </a>
                    <a href="/ketik" class="menu-item-cyber">
                        <span class="menu-icon-cyber">⌨️</span>
                        <span class="menu-label-cyber">Ketik</span>
                    </a>
                    <a href="/konversi" class="menu-item-cyber">
                        <span class="menu-icon-cyber">🔄</span>
                        <span class="menu-label-cyber">Konversi</span>
                    </a>
                </div>
            </nav>

            <footer class="text-center py-6 mt-8 fade-cyber" style="animation-delay: 0.6s;">
                <p style="color: rgba(0,255,255,0.12); font-size: 0.55rem; font-family: 'Orbitron', sans-serif; letter-spacing: 3px;">
                    ⚡ NEXUS CYBER UTILITY • DATA IN MEMORY • MADE WITH ❤️ ⚡
                </p>
            </footer>
        </div>
    </div>

    <script>
        // ===== PARTICLES =====
        function createParticles() {
            const container = document.getElementById('particles');
            for(let i = 0; i < 30; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.width = (Math.random() * 3 + 1) + 'px';
                particle.style.height = particle.style.width;
                particle.style.animationDuration = (Math.random() * 10 + 5) + 's';
                particle.style.animationDelay = (Math.random() * 10) + 's';
                particle.style.opacity = Math.random() * 0.3 + 0.1;
                container.appendChild(particle);
            }
        }
        createParticles();

        // ===== GLITCH EFFECT ON MENU =====
        document.querySelectorAll('.menu-item-cyber').forEach(item => {
            item.addEventListener('mouseenter', function() {
                this.style.animation = 'glitchText 0.3s ease';
                setTimeout(() => {
                    this.style.animation = '';
                }, 300);
            });
        });
    </script>
</body>
</html>
"""

# ==========================================
# TEMPLATE FULL PAGE UNTUK SETIAP FITUR
# ==========================================
PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXUS • {title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
        
        * {{ 
            font-family: 'Rajdhani', sans-serif;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            background: #05050a;
            min-height: 100vh;
            color: #00ffff;
            overflow-x: hidden;
        }}
        
        .cyber-bg {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            background: 
                radial-gradient(circle at 20% 30%, rgba(0, 255, 255, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 80% 70%, rgba(255, 0, 255, 0.08) 0%, transparent 50%);
            animation: cyberPulse 6s ease-in-out infinite alternate;
        }}
        
        @keyframes cyberPulse {{
            0% {{ opacity: 0.6; transform: scale(1); }}
            100% {{ opacity: 1; transform: scale(1.05); }}
        }}
        
        .cyber-grid {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            background-image: 
                linear-gradient(rgba(0, 255, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 255, 0.03) 1px, transparent 1px);
            background-size: 50px 50px;
            animation: gridMove 15s linear infinite;
        }}
        
        @keyframes gridMove {{
            0% {{ transform: translate(0, 0); }}
            100% {{ transform: translate(50px, 50px); }}
        }}
        
        .scanline {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            background: repeating-linear-gradient(
                0deg,
                transparent,
                transparent 2px,
                rgba(0, 255, 255, 0.02) 2px,
                rgba(0, 255, 255, 0.02) 4px
            );
            pointer-events: none;
            animation: scanMove 8s linear infinite;
        }}
        
        @keyframes scanMove {{
            0% {{ transform: translateY(0); }}
            100% {{ transform: translateY(100%); }}
        }}
        
        .glass-cyber {{
            background: rgba(0, 20, 30, 0.6);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(0, 255, 255, 0.15);
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.05), inset 0 0 30px rgba(0, 255, 255, 0.02);
            position: relative;
            z-index: 1;
        }}
        
        .glass-cyber::before {{
            content: '';
            position: absolute;
            top: -1px;
            left: 20%;
            right: 20%;
            height: 1px;
            background: linear-gradient(90deg, transparent, #00ffff, transparent);
            animation: neonLine 3s ease-in-out infinite;
        }}
        
        @keyframes neonLine {{
            0%, 100% {{ opacity: 0.2; }}
            50% {{ opacity: 1; }}
        }}
        
        .glass-card-cyber {{
            background: rgba(0, 20, 30, 0.4);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 255, 255, 0.08);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            z-index: 1;
        }}
        
        .glass-card-cyber:hover {{
            transform: translateY(-4px);
            border-color: rgba(0, 255, 255, 0.3);
            box-shadow: 0 0 40px rgba(0, 255, 255, 0.05);
        }}
        
        .cyber-text {{
            background: linear-gradient(135deg, #00ffff 0%, #ff00ff 50%, #00ffff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            filter: drop-shadow(0 0 20px rgba(0, 255, 255, 0.3));
        }}
        
        .cyber-value {{
            font-family: 'Orbitron', sans-serif;
            color: #00ffff;
            text-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
        }}
        
        .btn-cyber {{
            background: linear-gradient(135deg, #00ffff, #0088ff);
            color: #05050a;
            font-weight: 700;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            text-transform: uppercase;
            letter-spacing: 2px;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
        }}
        
        .btn-cyber::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.2), transparent);
            transform: rotate(45deg);
            transition: all 0.5s ease;
        }}
        
        .btn-cyber:hover::before {{
            left: 100%;
        }}
        
        .btn-cyber:hover {{
            transform: scale(1.03);
            box-shadow: 0 0 40px rgba(0, 255, 255, 0.3);
        }}
        
        .btn-cyber:active {{
            transform: scale(0.95);
        }}
        
        .btn-back {{
            background: rgba(0, 255, 255, 0.05);
            border: 1px solid rgba(0, 255, 255, 0.1);
            color: #00ffff;
            padding: 10px 24px;
            border-radius: 8px;
            transition: all 0.3s ease;
            text-decoration: none;
            font-family: 'Orbitron', sans-serif;
            font-size: 0.7rem;
            letter-spacing: 2px;
            display: inline-block;
        }}
        
        .btn-back:hover {{
            background: rgba(0, 255, 255, 0.1);
            border-color: #00ffff;
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.1);
            transform: translateX(-4px);
        }}
        
        .input-cyber {{
            background: rgba(0, 10, 20, 0.6);
            border: 1px solid rgba(0, 255, 255, 0.15);
            color: #00ffff;
            transition: all 0.3s ease;
            border-radius: 8px;
            padding: 12px 16px;
            width: 100%;
        }}
        
        .input-cyber:focus {{
            border-color: #00ffff;
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.1), inset 0 0 20px rgba(0, 255, 255, 0.05);
            outline: none;
            background: rgba(0, 10, 20, 0.8);
        }}
        
        .input-cyber::placeholder {{
            color: rgba(0, 255, 255, 0.3);
        }}
        
        select.input-cyber option {{
            background: #0a0a1a;
            color: #00ffff;
        }}
        
        .cyber-label {{
            font-family: 'Orbitron', sans-serif;
            font-size: 0.6rem;
            letter-spacing: 2px;
            color: rgba(0, 255, 255, 0.4);
            text-transform: uppercase;
        }}
        
        .fade-cyber {{
            animation: fadeCyber 0.6s ease forwards;
        }}
        
        @keyframes fadeCyber {{
            from {{ opacity: 0; transform: translateY(20px) scale(0.95); filter: blur(5px); }}
            to {{ opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }}
        }}
        
        .cyber-title-page {{
            font-family: 'Orbitron', sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
        }}
        
        @media (max-width: 640px) {{
            .cyber-title-page {{ font-size: 1.3rem; }}
        }}
        
        ::-webkit-scrollbar {{ width: 4px; }}
        ::-webkit-scrollbar-track {{ background: rgba(0,255,255,0.02); }}
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(135deg, #00ffff, #0088ff);
            border-radius: 10px;
        }}
        
        .float-cyber {{
            animation: floatCyber 4s ease-in-out infinite;
        }}
        
        @keyframes floatCyber {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-6px); }}
        }}
    </style>
</head>
<body>
    <div class="cyber-bg"></div>
    <div class="cyber-grid"></div>
    <div class="scanline"></div>

    <div class="relative z-10 p-4 md:p-6 min-h-screen">
        <div class="max-w-2xl mx-auto">
            <!-- BACK BUTTON & HEADER -->
            <div class="flex items-center justify-between mb-6 fade-cyber">
                <a href="/" class="btn-back">← KEMBALI</a>
                <div class="text-right float-cyber">
                    <span class="text-3xl">{icon}</span>
                    <h1 class="cyber-title-page cyber-text">{title}</h1>
                </div>
            </div>

            <!-- KONTEN -->
            <div class="fade-cyber" style="animation-delay: 0.2s;">
                {content}
            </div>

            <!-- FOOTER -->
            <footer class="text-center py-6 mt-8 fade-cyber" style="animation-delay: 0.4s;">
                <p style="color: rgba(0,255,255,0.08); font-size: 0.5rem; font-family: 'Orbitron', sans-serif; letter-spacing: 3px;">
                    ⚡ NEXUS CYBER • DATA IN MEMORY ⚡
                </p>
            </footer>
        </div>
    </div>
</body>
</html>
"""

# ==========================================
# ROUTE UNTUK SETIAP HALAMAN (FULL PAGE)
# ==========================================
@app.route('/')
def index():
    return HOME_PAGE

@app.route('/ucapan')
def ucapan():
    content = """
    <div class="glass-cyber rounded-2xl p-6 md:p-8">
        <form method="POST" action="/ucapan" class="space-y-4">
            <input type="text" name="nama" placeholder="Nama penerima" class="input-cyber" required>
            <input type="text" name="acara" placeholder="Jenis acara" class="input-cyber" required>
            <textarea name="pesan" rows="3" placeholder="Pesan ucapan..." class="input-cyber" required></textarea>
            <button type="submit" class="btn-cyber">✨ Buat Kartu</button>
        </form>
        <div class="mt-6 space-y-4">
            {% for item in store.ucapan %}
            <div class="glass-card-cyber p-4 rounded-xl border border-cyan-500/20">
                <p class="font-semibold text-cyan-300">Untuk: {{ item.nama }}</p>
                <p class="text-pink-300">Acara: {{ item.acara }}</p>
                <p class="text-gray-300 italic">"{{ item.pesan }}"</p>
                <small style="color: rgba(0,255,255,0.3);">{{ item.waktu }}</small>
            </div>
            {% endfor %}
        </div>
    </div>
    """
    return render_template_string(PAGE_TEMPLATE.format(title='Kartu Ucapan', icon='🎉', content=content), store=data_store)

@app.route('/pesan')
def pesan():
    content = """
    <div class="glass-cyber rounded-2xl p-6 md:p-8">
        <form method="POST" action="/pesan" class="space-y-4">
            <input type="text" name="judul" placeholder="Judul (opsional)" class="input-cyber">
            <textarea name="isi" rows="4" placeholder="Tulis pesan rahasia..." class="input-cyber" required></textarea>
            <button type="submit" class="btn-cyber">🤫 Kirim Rahasia</button>
        </form>
        <div class="mt-6 space-y-4">
            {% for item in store.pesan %}
            <div class="glass-card-cyber p-4 rounded-xl border border-pink-500/20">
                <p class="text-gray-300">{{ item.isi }}</p>
                <small style="color: rgba(0,255,255,0.3);">#{{ item.id }} • {{ item.waktu }}</small>
            </div>
            {% endfor %}
        </div>
    </div>
    """
    return render_template_string(PAGE_TEMPLATE.format(title='Pesan Rahasia', icon='💌', content=content), store=data_store)

@app.route('/kuis')
def kuis():
    content = """
    <div class="glass-cyber rounded-2xl p-6 md:p-8">
        <form method="POST" action="/kuis" class="space-y-4">
            <div class="glass-card-cyber p-4 rounded-xl border border-cyan-500/20">
                <p class="text-gray-300">Pertanyaan: Apa makanan favorit saya?</p>
            </div>
            <input type="text" name="jawaban" placeholder="Jawaban..." class="input-cyber" required>
            <button type="submit" class="btn-cyber">Kirim Jawaban</button>
        </form>
        <div class="mt-6">
            <p class="text-gray-400 cyber-label">Skor Anda: <span class="text-cyan-300 font-bold text-3xl cyber-value">{{ session.get('skor_kuis', 0) }}</span></p>
            {% if session.get('last_answer') %}
            <div class="glass-card-cyber p-4 rounded-xl mt-3 border border-cyan-500/20">
                <p class="text-gray-300">{{ session.get('last_answer') }}</p>
            </div>
            {% endif %}
        </div>
    </div>
    """
    return render_template_string(PAGE_TEMPLATE.format(title='Kuis', icon='🧠', content=content), session=session)

@app.route('/qr')
def qr():
    content = """
    <div class="glass-cyber rounded-2xl p-6 md:p-8">
        <form method="POST" action="/qr" class="space-y-4">
            <input type="url" name="url" placeholder="Masukkan URL..." class="input-cyber" required>
            <button type="submit" class="btn-cyber">🔗 Buat QR</button>
        </form>
        {% if session.get('qr_result') %}
        <div class="mt-6 glass-card-cyber p-4 rounded-xl border border-cyan-500/20 text-center">
            <p class="text-gray-300 break-all">Short URL: <a href="{{ session.qr_result.short }}" target="_blank" class="text-cyan-300 hover:underline">{{ session.qr_result.short }}</a></p>
            <img src="data:image/png;base64,{{ session.qr_result.qr }}" class="mx-auto mt-3 w-48 h-48" alt="QR Code">
        </div>
        {% endif %}
    </div>
    """
    return render_template_string(PAGE_TEMPLATE.format(title='QR & Short URL', icon='📱', content=content), session=session)

@app.route('/keuangan')
def keuangan():
    total_pengeluaran = sum(item['jumlah'] for item in data_store['keuangan'] if item['jenis'] == 'pengeluaran')
    total_simpanan = sum(item['jumlah'] for item in data_store['keuangan'] if item['jenis'] == 'simpanan')
    
    content = f"""
    <div class="glass-cyber rounded-2xl p-6 md:p-8">
        <form method="POST" action="/keuangan" class="space-y-4">
            <select name="jenis" class="input-cyber">
                <option value="pengeluaran">Pengeluaran</option>
                <option value="simpanan">Simpanan</option>
            </select>
            <input type="number" name="jumlah" placeholder="Jumlah (Rp)" class="input-cyber" required>
            <input type="text" name="keterangan" placeholder="Keterangan" class="input-cyber">
            <button type="submit" class="btn-cyber">💰 Tambah Catatan</button>
        </form>
        <div class="mt-6">
            <div class="grid grid-cols-2 gap-4 mb-4">
                <div class="glass-card-cyber p-4 rounded-xl text-center">
                    <p class="cyber-label">Pengeluaran</p>
                    <p class="text-2xl font-bold text-pink-400 cyber-value">Rp {total_pengeluaran:,.0f}</p>
                </div>
                <div class="glass-card-cyber p-4 rounded-xl text-center">
                    <p class="cyber-label">Simpanan</p>
                    <p class="text-2xl font-bold text-cyan-400 cyber-value">Rp {total_simpanan:,.0f}</p>
                </div>
            </div>
            <div class="space-y-2 max-h-60 overflow-y-auto">
                {% for item in store.keuangan[-10:]|reverse %}
                <div class="glass-card-cyber p-3 rounded-xl text-sm flex justify-between items-center">
                    <span>{{ item.jenis }} • {{ item.keterangan }}</span>
                    <span class="font-bold {% if item.jenis == 'pengeluaran' %}text-pink-400{% else %}text-cyan-400{% endif %}">Rp {{ "%.0f"|format(item.jumlah) }}</span>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
    """
    return render_template_string(PAGE_TEMPLATE.format(title='Catatan Keuangan', icon='💰', content=content), store=data_store)

@app.route('/hitung')
def hitung():
    content = """
    <div class="glass-cyber rounded-2xl p-6 md:p-8">
        <form method="POST" action="/hitung" class="space-y-4">
            <input type="text" name="acara" placeholder="Nama acara" class="input-cyber" required>
            <input type="date" name="tanggal" class="input-cyber" required>
            <button type="submit" class="btn-cyber">⏱️ Hitung Hari</button>
        </form>
        <div class="mt-6 space-y-4">
            {% for item in store.hitung %}
            <div class="glass-card-cyber p-4 rounded-xl border border-cyan-500/20">
                <p class="font-semibold">{{ item.acara }}</p>
                <p class="text-3xl font-bold text-cyan-300 cyber-value">{{ item.sisa_hari }} hari lagi</p>
                <small style="color: rgba(0,255,255,0.3);">{{ item.tanggal }}</small>
            </div>
            {% endfor %}
        </div>
    </div>
    """
    return render_template_string(PAGE_TEMPLATE.format(title='Penghitung Hari', icon='⏳', content=content), store=data_store)

@app.route('/teks')
def teks():
    content = """
    <div class="glass-cyber rounded-2xl p-6 md:p-8">
        <form method="POST" action="/teks" class="space-y-4">
            <input type="text" name="teks" placeholder="Masukkan teks..." class="input-cyber" required>
            <select name="gaya" class="input-cyber">
                <option value="esthetic">Estetik (𝓪𝓫𝓬)</option>
                <option value="upside">Terbalik (ɐqɔ)</option>
            </select>
            <button type="submit" class="btn-cyber">✨ Ubah Gaya</button>
        </form>
        {% if session.get('styled_text') %}
        <div class="mt-6 glass-card-cyber p-4 rounded-xl border border-cyan-500/20 text-center">
            <p class="text-2xl" style="color: #00ffff;">{{ session.styled_text }}</p>
        </div>
        {% endif %}
    </div>
    """
    return render_template_string(PAGE_TEMPLATE.format(title='Pengubah Teks', icon='✨', content=content), session=session)

@app.route('/favorit')
def favorit():
    content = """
    <div class="glass-cyber rounded-2xl p-6 md:p-8">
        <form method="POST" action="/favorit" class="space-y-4">
            <input type="text" name="judul" placeholder="Judul" class="input-cyber" required>
            <input type="url" name="url" placeholder="URL (opsional)" class="input-cyber">
            <textarea name="catatan" rows="2" placeholder="Catatan..." class="input-cyber"></textarea>
            <button type="submit" class="btn-cyber">⭐ Simpan</button>
        </form>
        <div class="mt-6 space-y-3">
            {% for item in store.favorit %}
            <div class="glass-card-cyber p-4 rounded-xl border border-cyan-500/20">
                <p class="font-semibold">{{ item.judul }}</p>
                {% if item.url %}<a href="{{ item.url }}" target="_blank" class="text-cyan-300 text-sm hover:underline">{{ item.url }}</a>{% endif %}
                <p class="text-gray-400 text-sm">{{ item.catatan }}</p>
            </div>
            {% endfor %}
        </div>
    </div>
    """
    return render_template_string(PAGE_TEMPLATE.format(title='Favorit & Bacaan', icon='⭐', content=content), store=data_store)

@app.route('/ketik')
def ketik():
    content = """
    <div class="glass-cyber rounded-2xl p-6 md:p-8">
        <div class="glass-card-cyber p-4 rounded-xl mb-4 border border-cyan-500/20">
            <p class="text-gray-300 text-sm">Ketik kalimat ini secepat mungkin untuk mengukur kecepatan mengetik Anda.</p>
        </div>
        <form method="POST" action="/ketik" class="space-y-4">
            <input type="text" name="input_ketik" placeholder="Mulai mengetik..." class="input-cyber" required>
            <button type="submit" class="btn-cyber">🚀 Kirim & Hitung</button>
        </form>
        {% if session.get('hasil_ketik') %}
        <div class="mt-6 glass-card-cyber p-4 rounded-xl border border-cyan-500/20">
            <p class="text-gray-300">Kecepatan: <span class="text-cyan-300 font-bold text-xl cyber-value">{{ session.hasil_ketik }}</span></p>
        </div>
        {% endif %}
    </div>
    """
    return render_template_string(PAGE_TEMPLATE.format(title='Kecepatan Ketik', icon='⌨️', content=content), session=session)

@app.route('/konversi')
def konversi():
    content = """
    <div class="glass-cyber rounded-2xl p-6 md:p-8">
        <form method="POST" action="/konversi" class="space-y-4">
            <div class="grid grid-cols-2 gap-3">
                <input type="number" name="nilai" placeholder="Nilai" class="input-cyber" required>
                <select name="dari" class="input-cyber">
                    <option value="usd">USD</option>
                    <option value="eur">EUR</option>
                    <option value="idr">IDR</option>
                </select>
                <select name="ke" class="input-cyber">
                    <option value="usd">USD</option>
                    <option value="eur">EUR</option>
                    <option value="idr">IDR</option>
                </select>
                <select name="jenis_konversi" class="input-cyber">
                    <option value="mata_uang">Mata Uang</option>
                    <option value="panjang">Panjang (m/km)</option>
                    <option value="berat">Berat (kg/g)</option>
                </select>
            </div>
            <button type="submit" class="btn-cyber">🔄 Konversi</button>
        </form>
        {% if session.get('hasil_konversi') %}
        <div class="mt-6 glass-card-cyber p-4 rounded-xl border border-cyan-500/20 text-center">
            <p class="text-gray-300">Hasil: <span class="text-cyan-300 font-bold text-xl cyber-value">{{ session.hasil_konversi }}</span></p>
        </div>
        {% endif %}
    </div>
    """
    return render_template_string(PAGE_TEMPLATE.format(title='Konversi', icon='🔄', content=content), session=session)

# ==========================================
# ROUTE HANDLER POST
# ==========================================
@app.route('/ucapan', methods=['POST'])
def handle_ucapan():
    data_store['ucapan'].append({
        'nama': request.form['nama'],
        'acara': request.form['acara'],
        'pesan': request.form['pesan'],
        'waktu': datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    })
    return redirect(url_for('ucapan'))

@app.route('/pesan', methods=['POST'])
def handle_pesan():
    data_store['pesan'].append({
        'id': len(data_store['pesan']) + 1,
        'isi': request.form['isi'],
        'waktu': datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    })
    return redirect(url_for('pesan'))

@app.route('/kuis', methods=['POST'])
def handle_kuis():
    jawaban = request.form['jawaban'].lower().strip()
    if jawaban == 'nasi goreng':
        skor = session.get('skor_kuis', 0) + 10
        session['skor_kuis'] = skor
        session['last_answer'] = '✅ Benar! +10 poin'
    else:
        session['last_answer'] = '❌ Kurang tepat, coba lagi!'
    return redirect(url_for('kuis'))

@app.route('/qr', methods=['POST'])
def handle_qr():
    url = request.form['url']
    short = hashlib.md5(url.encode()).hexdigest()[:8]
    qr = generate_qr(url)
    session['qr_result'] = {'short': f'https://short.link/{short}', 'qr': qr}
    return redirect(url_for('qr'))

@app.route('/keuangan', methods=['POST'])
def handle_keuangan():
    data_store['keuangan'].append({
        'jenis': request.form['jenis'],
        'jumlah': float(request.form['jumlah']),
        'keterangan': request.form['keterangan'] or '-',
        'waktu': datetime.datetime.now().strftime('%d/%m')
    })
    return redirect(url_for('keuangan'))

@app.route('/hitung', methods=['POST'])
def handle_hitung():
    tanggal = datetime.datetime.strptime(request.form['tanggal'], '%Y-%m-%d').date()
    sisa = (tanggal - datetime.date.today()).days
    data_store['hitung'].append({
        'acara': request.form['acara'],
        'tanggal': request.form['tanggal'],
        'sisa_hari': max(0, sisa)
    })
    return redirect(url_for('hitung'))

@app.route('/teks', methods=['POST'])
def handle_teks():
    teks = request.form['teks']
    gaya = request.form['gaya']
    session['styled_text'] = stylize_text(teks, gaya)
    return redirect(url_for('teks'))

@app.route('/favorit', methods=['POST'])
def handle_favorit():
    data_store['favorit'].append({
        'judul': request.form['judul'],
        'url': request.form['url'],
        'catatan': request.form['catatan']
    })
    return redirect(url_for('favorit'))

@app.route('/ketik', methods=['POST'])
def handle_ketik():
    start = time.time()
    input_teks = request.form['input_ketik']
    if len(input_teks) == 0:
        session['hasil_ketik'] = "Silakan ketik sesuatu!"
    else:
        elapsed = time.time() - start
        wpm = (len(input_teks.split()) / elapsed) * 60
        session['hasil_ketik'] = f"{wpm:.1f} kata/menit ({elapsed:.2f} detik)"
    return redirect(url_for('ketik'))

@app.route('/konversi', methods=['POST'])
def handle_konversi():
    nilai = float(request.form['nilai'])
    dari = request.form['dari']
    ke = request.form['ke']
    jenis = request.form['jenis_konversi']
    
    kurs = {'usd': 1, 'eur': 0.92, 'idr': 15500}
    if jenis == 'mata_uang':
        hasil = (nilai / kurs[dari]) * kurs[ke]
        session['hasil_konversi'] = f"{nilai:.2f} {dari.upper()} = {hasil:.2f} {ke.upper()}"
    elif jenis == 'panjang':
        if dari == 'm' and ke == 'km':
            session['hasil_konversi'] = f"{nilai} m = {nilai/1000:.3f} km"
        elif dari == 'km' and ke == 'm':
            session['hasil_konversi'] = f"{nilai} km = {nilai*1000:.0f} m"
        else:
            session['hasil_konversi'] = f"{nilai} {dari} = {nilai} {ke}"
    elif jenis == 'berat':
        if dari == 'kg' and ke == 'g':
            session['hasil_konversi'] = f"{nilai} kg = {nilai*1000:.0f} g"
        elif dari == 'g' and ke == 'kg':
            session['hasil_konversi'] = f"{nilai} g = {nilai/1000:.3f} kg"
        else:
            session['hasil_konversi'] = f"{nilai} {dari} = {nilai} {ke}"
    return redirect(url_for('konversi'))

# ==========================================
# JALANKAN APLIKASI
# ==========================================
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
