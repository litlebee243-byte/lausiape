# ==========================================
# PROJECT: NEXUS CYBER UTILITY SUITE 
# FILE: app.py
# VERSION: CYBER v4.0
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
# TEMPLATE CYBERPUNK
# ==========================================
BASE_TEMPLATE = """
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
        
        /* CYBERPUNK BACKGROUND */
        .cyber-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            background: 
                radial-gradient(circle at 20% 30%, rgba(0, 255, 255, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 80% 70%, rgba(255, 0, 255, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 50% 50%, rgba(0, 100, 255, 0.03) 0%, transparent 70%);
            animation: cyberPulse 6s ease-in-out infinite alternate;
        }
        
        @keyframes cyberPulse {
            0% { opacity: 0.5; transform: scale(1); }
            100% { opacity: 1; transform: scale(1.05); }
        }
        
        /* Grid Overlay Cyber */
        .cyber-grid {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            background-image: 
                linear-gradient(rgba(0, 255, 255, 0.02) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 255, 0.02) 1px, transparent 1px);
            background-size: 50px 50px;
            animation: gridMove 20s linear infinite;
        }
        
        @keyframes gridMove {
            0% { transform: translate(0, 0); }
            100% { transform: translate(50px, 50px); }
        }
        
        /* Scanline Effect */
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
                rgba(0, 255, 255, 0.01) 2px,
                rgba(0, 255, 255, 0.01) 4px
            );
            pointer-events: none;
            animation: scanMove 10s linear infinite;
        }
        
        @keyframes scanMove {
            0% { transform: translateY(0); }
            100% { transform: translateY(100%); }
        }
        
        /* GLASS CYBER */
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
            0%, 100% { opacity: 0.3; }
            50% { opacity: 1; }
        }
        
        .glass-card-cyber {
            background: rgba(0, 20, 30, 0.4);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(0, 255, 255, 0.08);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            z-index: 1;
        }
        
        .glass-card-cyber:hover {
            transform: translateY(-4px);
            border-color: rgba(0, 255, 255, 0.3);
            box-shadow: 0 0 40px rgba(0, 255, 255, 0.05);
        }
        
        /* CYBER GRADIENT TEXT */
        .cyber-text {
            background: linear-gradient(135deg, #00ffff 0%, #ff00ff 50%, #00ffff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: none;
            filter: drop-shadow(0 0 20px rgba(0, 255, 255, 0.3));
        }
        
        .cyber-text-glow {
            color: #00ffff;
            text-shadow: 0 0 10px rgba(0, 255, 255, 0.3), 0 0 30px rgba(0, 255, 255, 0.1);
        }
        
        /* CYBER BUTTON */
        .btn-cyber {
            background: linear-gradient(135deg, #00ffff, #0088ff);
            color: #05050a;
            font-weight: 700;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            text-transform: uppercase;
            letter-spacing: 2px;
            border: none;
        }
        
        .btn-cyber::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
            transform: rotate(45deg);
            transition: all 0.5s ease;
        }
        
        .btn-cyber:hover::before {
            left: 100%;
        }
        
        .btn-cyber:hover {
            transform: scale(1.03);
            box-shadow: 0 0 40px rgba(0, 255, 255, 0.3);
        }
        
        /* CYBER INPUT */
        .input-cyber {
            background: rgba(0, 10, 20, 0.6);
            border: 1px solid rgba(0, 255, 255, 0.15);
            color: #00ffff;
            transition: all 0.3s ease;
            border-radius: 8px;
            padding: 12px 16px;
            width: 100%;
        }
        
        .input-cyber:focus {
            border-color: #00ffff;
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.1), inset 0 0 20px rgba(0, 255, 255, 0.05);
            outline: none;
            background: rgba(0, 10, 20, 0.8);
        }
        
        .input-cyber::placeholder {
            color: rgba(0, 255, 255, 0.3);
        }
        
        select.input-cyber option {
            background: #0a0a1a;
            color: #00ffff;
        }
        
        /* ==========================================
           MENU NAVIGASI CYBER
           ========================================== */
        .menu-cyber {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 8px;
            padding: 6px;
        }
        
        @media (max-width: 640px) {
            .menu-cyber {
                grid-template-columns: repeat(4, 1fr);
                gap: 6px;
            }
        }
        
        @media (max-width: 400px) {
            .menu-cyber {
                grid-template-columns: repeat(3, 1fr);
                gap: 4px;
            }
        }
        
        .menu-item-cyber {
            background: rgba(0, 20, 30, 0.3);
            border: 1px solid rgba(0, 255, 255, 0.08);
            border-radius: 12px;
            padding: 12px 6px;
            text-align: center;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            cursor: pointer;
            text-decoration: none;
            color: rgba(0, 255, 255, 0.6);
            position: relative;
            overflow: hidden;
        }
        
        .menu-item-cyber::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.05), transparent);
            transition: all 0.5s ease;
        }
        
        .menu-item-cyber:hover::before {
            left: 100%;
        }
        
        .menu-item-cyber:hover {
            transform: translateY(-4px) scale(1.03);
            border-color: rgba(0, 255, 255, 0.3);
            background: rgba(0, 255, 255, 0.05);
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.05);
            color: #00ffff;
        }
        
        .menu-item-cyber.active {
            border-color: #00ffff;
            background: rgba(0, 255, 255, 0.08);
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.1);
            color: #00ffff;
        }
        
        .menu-item-cyber.active .menu-icon-cyber {
            transform: scale(1.1);
            filter: drop-shadow(0 0 10px rgba(0, 255, 255, 0.3));
        }
        
        .menu-icon-cyber {
            font-size: 1.8rem;
            display: block;
            margin-bottom: 2px;
            transition: all 0.3s ease;
        }
        
        .menu-label-cyber {
            font-size: 0.6rem;
            font-weight: 600;
            letter-spacing: 1px;
            text-transform: uppercase;
            font-family: 'Orbitron', sans-serif;
        }
        
        @media (max-width: 640px) {
            .menu-icon-cyber { font-size: 1.4rem; }
            .menu-label-cyber { font-size: 0.5rem; }
            .menu-item-cyber { padding: 8px 4px; }
        }
        
        /* WELCOME SCREEN CYBER */
        .welcome-cyber {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 9999;
            background: #05050a;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: cyberIn 1s ease;
        }
        
        @keyframes cyberIn {
            from { opacity: 0; transform: scale(0.95); }
            to { opacity: 1; transform: scale(1); }
        }
        
        .welcome-content-cyber {
            text-align: center;
            animation: cyberFloat 4s ease-in-out infinite;
            position: relative;
            z-index: 1;
        }
        
        @keyframes cyberFloat {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        .cyber-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 5rem;
            font-weight: 900;
            background: linear-gradient(135deg, #00ffff 0%, #ff00ff 50%, #00ffff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: none;
            filter: drop-shadow(0 0 40px rgba(0, 255, 255, 0.3));
            letter-spacing: 8px;
        }
        
        @media (max-width: 640px) {
            .cyber-title { font-size: 3rem; letter-spacing: 4px; }
        }
        
        .cyber-sub {
            color: rgba(0, 255, 255, 0.5);
            font-weight: 300;
            letter-spacing: 12px;
            text-transform: uppercase;
            font-size: 0.9rem;
            font-family: 'Orbitron', sans-serif;
        }
        
        .btn-enter-cyber {
            background: linear-gradient(135deg, #00ffff, #0088ff);
            padding: 16px 48px;
            border-radius: 8px;
            color: #05050a;
            font-weight: 700;
            font-size: 1.1rem;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.2);
            letter-spacing: 4px;
            text-transform: uppercase;
            font-family: 'Orbitron', sans-serif;
        }
        
        .btn-enter-cyber:hover {
            transform: scale(1.05);
            box-shadow: 0 0 60px rgba(0, 255, 255, 0.4);
        }
        
        /* TYPOGRAPHY CYBER */
        .cyber-label {
            font-family: 'Orbitron', sans-serif;
            font-size: 0.7rem;
            letter-spacing: 2px;
            color: rgba(0, 255, 255, 0.5);
            text-transform: uppercase;
        }
        
        .cyber-value {
            font-family: 'Orbitron', sans-serif;
            color: #00ffff;
            text-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
        }
        
        /* SCROLLBAR */
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: rgba(0,255,255,0.02); }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #00ffff, #0088ff);
            border-radius: 10px;
        }
        
        .fade-cyber {
            animation: fadeCyber 0.6s ease forwards;
        }
        
        @keyframes fadeCyber {
            from { opacity: 0; transform: translateY(20px); filter: blur(5px); }
            to { opacity: 1; transform: translateY(0); filter: blur(0); }
        }
        
        /* CYBER DIVIDER */
        .cyber-divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.2), transparent);
            margin: 20px 0;
        }
        
        /* GLITCH EFFECT */
        .glitch {
            animation: glitch 3s infinite;
        }
        
        @keyframes glitch {
            2%, 64% { transform: translate(2px, 0) skew(0deg); }
            4%, 60% { transform: translate(-2px, 0) skew(0deg); }
            62% { transform: translate(0, 0) skew(5deg); }
        }
    </style>
</head>
<body>
    <!-- CYBER BACKGROUND -->
    <div class="cyber-bg"></div>
    <div class="cyber-grid"></div>
    <div class="scanline"></div>

    <!-- WELCOME SCREEN CYBER -->
    <div id="welcomeScreen" class="welcome-cyber">
        <div class="welcome-content-cyber px-6">
            <div class="text-7xl mb-4 glitch">⚡</div>
            <h1 class="cyber-title">NEXUS</h1>
            <p class="cyber-sub mb-6">Utility Suite • Cyber</p>
            <p class="text-gray-400 mb-8 max-w-md mx-auto text-sm" style="color: rgba(0,255,255,0.4);">
                <span class="cyber-label">>> SYSTEM READY <<</span><br>
                10 fitur canggih dalam satu platform
            </p>
            <button onclick="enterNexus()" class="btn-enter-cyber">
                ⚡ ENTER NEXUS ⚡
            </button>
            <p class="text-gray-600 text-xs mt-4" style="color: rgba(0,255,255,0.2);">v4.0 • CYBER EDITION</p>
        </div>
    </div>

    <!-- MAIN CONTENT -->
    <div id="mainContent" style="display: none;" class="relative z-10 p-4 md:p-6">
        <div class="max-w-6xl mx-auto">
            <!-- HEADER CYBER -->
            <header class="text-center py-6 fade-cyber">
                <h1 class="text-3xl md:text-5xl font-bold cyber-text font-['Orbitron'] tracking-wider">
                    ⚡ NEXUS
                </h1>
                <p class="text-sm md:text-base tracking-widest mt-1" style="color: rgba(0,255,255,0.4); font-family: 'Orbitron', sans-serif; letter-spacing: 4px;">
                    10 FITUR PREMIUM • SISTEM AKTIF
                </p>
            </header>

            <!-- MENU CYBER -->
            <nav class="glass-cyber rounded-2xl p-4 md:p-6 mb-8 fade-cyber">
                <div class="menu-cyber">
                    {% set menu_items = [
                        ('ucapan', '🎉', 'Ucapan'),
                        ('pesan', '💌', 'Pesan'),
                        ('kuis', '🧠', 'Kuis'),
                        ('qr', '📱', 'QR'),
                        ('keuangan', '💰', 'Keuangan'),
                        ('hitung', '⏳', 'Hitung'),
                        ('teks', '✨', 'Teks'),
                        ('favorit', '⭐', 'Favorit'),
                        ('ketik', '⌨️', 'Ketik'),
                        ('konversi', '🔄', 'Konversi')
                    ] %}
                    {% for id, icon, label in menu_items %}
                        <a href="/{{ id }}" 
                           class="menu-item-cyber {% if active == id %}active{% endif %}"
                           onclick="setActive('{{ id }}')">
                            <span class="menu-icon-cyber">{{ icon }}</span>
                            <span class="menu-label-cyber">{{ label }}</span>
                        </a>
                    {% endfor %}
                </div>
            </nav>

            <!-- KONTEN FITUR -->
            <div class="fade-cyber">
                {% block content %}{% endblock %}
            </div>

            <!-- FOOTER CYBER -->
            <footer class="text-center py-8 mt-12 border-t" style="border-color: rgba(0,255,255,0.05);">
                <p style="color: rgba(0,255,255,0.2); font-size: 0.7rem; font-family: 'Orbitron', sans-serif; letter-spacing: 2px;">
                    NEXUS CYBER UTILITY • DATA IN MEMORY • MADE WITH ❤️
                </p>
            </footer>
        </div>
    </div>

    <script>
        function enterNexus() {
            const welcome = document.getElementById('welcomeScreen');
            const main = document.getElementById('mainContent');
            welcome.style.opacity = '0';
            welcome.style.transition = 'opacity 0.8s ease';
            setTimeout(() => {
                welcome.style.display = 'none';
                main.style.display = 'block';
                main.style.animation = 'fadeCyber 0.8s ease';
            }, 800);
        }

        function setActive(id) {
            document.querySelectorAll('.menu-item-cyber').forEach(el => el.classList.remove('active'));
            const activeEl = document.querySelector(`.menu-item-cyber[href="/${id}"]`);
            if(activeEl) activeEl.classList.add('active');
        }

        document.addEventListener('DOMContentLoaded', function() {
            const path = window.location.pathname;
            const activeId = path.replace('/', '') || 'ucapan';
            setActive(activeId);
            
            // Cek apakah welcome sudah pernah ditampilkan
            if(!sessionStorage.getItem('nexus_entered')) {
                // Tampilkan welcome
            } else {
                document.getElementById('welcomeScreen').style.display = 'none';
                document.getElementById('mainContent').style.display = 'block';
            }
        });

        // Tandai sudah masuk
        function enterNexus() {
            sessionStorage.setItem('nexus_entered', 'true');
            const welcome = document.getElementById('welcomeScreen');
            const main = document.getElementById('mainContent');
            welcome.style.opacity = '0';
            welcome.style.transition = 'opacity 0.8s ease';
            setTimeout(() => {
                welcome.style.display = 'none';
                main.style.display = 'block';
                main.style.animation = 'fadeCyber 0.8s ease';
            }, 800);
        }
    </script>
</body>
</html>
"""

# ==========================================
# ROUTE UNTUK SETIAP HALAMAN
# ==========================================
@app.route('/')
def index():
    return redirect(url_for('page', page='ucapan'))

@app.route('/<page>')
def page(page):
    valid_pages = ['ucapan', 'pesan', 'kuis', 'qr', 'keuangan', 'hitung', 'teks', 'favorit', 'ketik', 'konversi']
    if page not in valid_pages:
        page = 'ucapan'
    
    contents = {
        'ucapan': """
        <section class="glass-card-cyber rounded-2xl p-6 md:p-8">
            <div class="flex items-center gap-3 mb-6">
                <span class="text-3xl">🎉</span>
                <h2 class="text-2xl font-bold cyber-text">Pembuat Kartu Ucapan</h2>
            </div>
            <form method="POST" action="/ucapan" class="space-y-4">
                <input type="text" name="nama" placeholder="Nama penerima" class="input-cyber" required>
                <input type="text" name="acara" placeholder="Jenis acara" class="input-cyber" required>
                <textarea name="pesan" rows="3" placeholder="Pesan ucapan..." class="input-cyber" required></textarea>
                <button type="submit" class="btn-cyber w-full py-3 rounded-xl font-semibold">✨ Buat Kartu</button>
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
        </section>
        """,
        'pesan': """
        <section class="glass-card-cyber rounded-2xl p-6 md:p-8">
            <div class="flex items-center gap-3 mb-6">
                <span class="text-3xl">💌</span>
                <h2 class="text-2xl font-bold cyber-text">Kotak Pesan Rahasia</h2>
            </div>
            <form method="POST" action="/pesan" class="space-y-4">
                <input type="text" name="judul" placeholder="Judul (opsional)" class="input-cyber">
                <textarea name="isi" rows="4" placeholder="Tulis pesan rahasia..." class="input-cyber" required></textarea>
                <button type="submit" class="btn-cyber w-full py-3 rounded-xl font-semibold">🤫 Kirim Rahasia</button>
            </form>
            <div class="mt-6 space-y-4">
                {% for item in store.pesan %}
                <div class="glass-card-cyber p-4 rounded-xl border border-pink-500/20">
                    <p class="text-gray-300">{{ item.isi }}</p>
                    <small style="color: rgba(0,255,255,0.3);">#{{ item.id }} • {{ item.waktu }}</small>
                </div>
                {% endfor %}
            </div>
        </section>
        """,
        'kuis': """
        <section class="glass-card-cyber rounded-2xl p-6 md:p-8">
            <div class="flex items-center gap-3 mb-6">
                <span class="text-3xl">🧠</span>
                <h2 class="text-2xl font-bold cyber-text">Kuis "Seberapa Kenal Kamu?"</h2>
            </div>
            <form method="POST" action="/kuis" class="space-y-4">
                <div class="glass-card-cyber p-4 rounded-xl border border-cyan-500/20">
                    <p class="text-gray-300">Pertanyaan: Apa makanan favorit saya?</p>
                </div>
                <input type="text" name="jawaban" placeholder="Jawaban..." class="input-cyber" required>
                <button type="submit" class="btn-cyber w-full py-3 rounded-xl font-semibold">Kirim Jawaban</button>
            </form>
            <div class="mt-6">
                <p class="text-gray-400">Skor Anda: <span class="text-cyan-300 font-bold text-2xl cyber-value">{{ session.get('skor_kuis', 0) }}</span></p>
                {% if session.get('last_answer') %}
                <div class="glass-card-cyber p-4 rounded-xl mt-3 border border-cyan-500/20">
                    <p class="text-gray-300">{{ session.get('last_answer') }}</p>
                </div>
                {% endif %}
            </div>
        </section>
        """,
        'qr': """
        <section class="glass-card-cyber rounded-2xl p-6 md:p-8">
            <div class="flex items-center gap-3 mb-6">
                <span class="text-3xl">📱</span>
                <h2 class="text-2xl font-bold cyber-text">Pembuat QR & Short URL</h2>
            </div>
            <form method="POST" action="/qr" class="space-y-4">
                <input type="url" name="url" placeholder="Masukkan URL..." class="input-cyber" required>
                <button type="submit" class="btn-cyber w-full py-3 rounded-xl font-semibold">🔗 Buat QR</button>
            </form>
            {% if session.get('qr_result') %}
            <div class="mt-6 glass-card-cyber p-4 rounded-xl border border-cyan-500/20 text-center">
                <p class="text-gray-300 break-all">Short URL: <a href="{{ session.qr_result.short }}" target="_blank" class="text-cyan-300 hover:underline">{{ session.qr_result.short }}</a></p>
                <img src="data:image/png;base64,{{ session.qr_result.qr }}" class="mx-auto mt-3 w-48 h-48" alt="QR Code">
            </div>
            {% endif %}
        </section>
        """,
        'keuangan': """
        <section class="glass-card-cyber rounded-2xl p-6 md:p-8">
            <div class="flex items-center gap-3 mb-6">
                <span class="text-3xl">💰</span>
                <h2 class="text-2xl font-bold cyber-text">Catatan Keuangan</h2>
            </div>
            <form method="POST" action="/keuangan" class="space-y-4">
                <select name="jenis" class="input-cyber">
                    <option value="pengeluaran">Pengeluaran</option>
                    <option value="simpanan">Simpanan</option>
                </select>
                <input type="number" name="jumlah" placeholder="Jumlah (Rp)" class="input-cyber" required>
                <input type="text" name="keterangan" placeholder="Keterangan" class="input-cyber">
                <button type="submit" class="btn-cyber w-full py-3 rounded-xl font-semibold">Tambah Catatan</button>
            </form>
            <div class="mt-6">
                <div class="grid grid-cols-2 gap-4 mb-4">
                    <div class="glass-card-cyber p-4 rounded-xl text-center">
                        <p class="text-gray-400 text-sm cyber-label">Pengeluaran</p>
                        <p class="text-2xl font-bold text-pink-400 cyber-value">Rp {{ "%.0f"|format(store.keuangan|selectattr('jenis', 'eq', 'pengeluaran')|map(attribute='jumlah')|sum) }}</p>
                    </div>
                    <div class="glass-card-cyber p-4 rounded-xl text-center">
                        <p class="text-gray-400 text-sm cyber-label">Simpanan</p>
                        <p class="text-2xl font-bold text-cyan-400 cyber-value">Rp {{ "%.0f"|format(store.keuangan|selectattr('jenis', 'eq', 'simpanan')|map(attribute='jumlah')|sum) }}</p>
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
        </section>
        """,
        'hitung': """
        <section class="glass-card-cyber rounded-2xl p-6 md:p-8">
            <div class="flex items-center gap-3 mb-6">
                <span class="text-3xl">⏳</span>
                <h2 class="text-2xl font-bold cyber-text">Penghitung Sisa Hari</h2>
            </div>
            <form method="POST" action="/hitung" class="space-y-4">
                <input type="text" name="acara" placeholder="Nama acara" class="input-cyber" required>
                <input type="date" name="tanggal" class="input-cyber" required>
                <button type="submit" class="btn-cyber w-full py-3 rounded-xl font-semibold">⏱️ Hitung Hari</button>
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
        </section>
        """,
        'teks': """
        <section class="glass-card-cyber rounded-2xl p-6 md:p-8">
            <div class="flex items-center gap-3 mb-6">
                <span class="text-3xl">✨</span>
                <h2 class="text-2xl font-bold cyber-text">Pengubah Teks Gaya Unik</h2>
            </div>
            <form method="POST" action="/teks" class="space-y-4">
                <input type="text" name="teks" placeholder="Masukkan teks..." class="input-cyber" required>
                <select name="gaya" class="input-cyber">
                    <option value="esthetic">Estetik (𝓪𝓫𝓬)</option>
                    <option value="upside">Terbalik (ɐqɔ)</option>
                </select>
                <button type="submit" class="btn-cyber w-full py-3 rounded-xl font-semibold">✨ Ubah Gaya</button>
            </form>
            {% if session.get('styled_text') %}
            <div class="mt-6 glass-card-cyber p-4 rounded-xl border border-cyan-500/20 text-center">
                <p class="text-2xl" style="color: #00ffff;">{{ session.styled_text }}</p>
            </div>
            {% endif %}
        </section>
        """,
        'favorit': """
        <section class="glass-card-cyber rounded-2xl p-6 md:p-8">
            <div class="flex items-center gap-3 mb-6">
                <span class="text-3xl">⭐</span>
                <h2 class="text-2xl font-bold cyber-text">Penyimpanan Favorit</h2>
            </div>
            <form method="POST" action="/favorit" class="space-y-4">
                <input type="text" name="judul" placeholder="Judul" class="input-cyber" required>
                <input type="url" name="url" placeholder="URL (opsional)" class="input-cyber">
                <textarea name="catatan" rows="2" placeholder="Catatan..." class="input-cyber"></textarea>
                <button type="submit" class="btn-cyber w-full py-3 rounded-xl font-semibold">⭐ Simpan</button>
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
        </section>
        """,
        'ketik': """
        <section class="glass-card-cyber rounded-2xl p-6 md:p-8">
            <div class="flex items-center gap-3 mb-6">
                <span class="text-3xl">⌨️</span>
                <h2 class="text-2xl font-bold cyber-text">Pengecekan Kecepatan Ketik</h2>
            </div>
            <div class="glass-card-cyber p-4 rounded-xl mb-4 border border-cyan-500/20">
                <p class="text-gray-300 text-sm">Ketik kalimat ini secepat mungkin untuk mengukur kecepatan mengetik Anda.</p>
            </div>
            <form method="POST" action="/ketik" class="space-y-4">
                <input type="text" name="input_ketik" placeholder="Mulai mengetik..." class="input-cyber" required>
                <button type="submit" class="btn-cyber w-full py-3 rounded-xl font-semibold">🚀 Kirim & Hitung</button>
            </form>
            {% if session.get('hasil_ketik') %}
            <div class="mt-6 glass-card-cyber p-4 rounded-xl border border-cyan-500/20">
                <p class="text-gray-300">Kecepatan: <span class="text-cyan-300 font-bold text-xl cyber-value">{{ session.hasil_ketik }}</span></p>
            </div>
            {% endif %}
        </section>
        """,
        'konversi': """
        <section class="glass-card-cyber rounded-2xl p-6 md:p-8">
            <div class="flex items-center gap-3 mb-6">
                <span class="text-3xl">🔄</span>
                <h2 class="text-2xl font-bold cyber-text">Konversi Mata Uang & Satuan</h2>
            </div>
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
                <button type="submit" class="btn-cyber w-full py-3 rounded-xl font-semibold">🔄 Konversi</button>
            </form>
            {% if session.get('hasil_konversi') %}
            <div class="mt-6 glass-card-cyber p-4 rounded-xl border border-cyan-500/20 text-center">
                <p class="text-gray-300">Hasil: <span class="text-cyan-300 font-bold text-xl cyber-value">{{ session.hasil_konversi }}</span></p>
            </div>
            {% endif %}
        </section>
        """
    }
    
    return render_template_string(BASE_TEMPLATE + contents.get(page, ''), 
                                   active=page, 
                                   store=data_store,
                                   session=session)

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
    return redirect(url_for('page', page='ucapan'))

@app.route('/pesan', methods=['POST'])
def handle_pesan():
    data_store['pesan'].append({
        'id': len(data_store['pesan']) + 1,
        'isi': request.form['isi'],
        'waktu': datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    })
    return redirect(url_for('page', page='pesan'))

@app.route('/kuis', methods=['POST'])
def handle_kuis():
    jawaban = request.form['jawaban'].lower().strip()
    if jawaban == 'nasi goreng':
        skor = session.get('skor_kuis', 0) + 10
        session['skor_kuis'] = skor
        session['last_answer'] = '✅ Benar! +10 poin'
    else:
        session['last_answer'] = '❌ Kurang tepat, coba lagi!'
    return redirect(url_for('page', page='kuis'))

@app.route('/qr', methods=['POST'])
def handle_qr():
    url = request.form['url']
    short = hashlib.md5(url.encode()).hexdigest()[:8]
    qr = generate_qr(url)
    session['qr_result'] = {'short': f'https://short.link/{short}', 'qr': qr}
    return redirect(url_for('page', page='qr'))

@app.route('/keuangan', methods=['POST'])
def handle_keuangan():
    data_store['keuangan'].append({
        'jenis': request.form['jenis'],
        'jumlah': float(request.form['jumlah']),
        'keterangan': request.form['keterangan'] or '-',
        'waktu': datetime.datetime.now().strftime('%d/%m')
    })
    return redirect(url_for('page', page='keuangan'))

@app.route('/hitung', methods=['POST'])
def handle_hitung():
    tanggal = datetime.datetime.strptime(request.form['tanggal'], '%Y-%m-%d').date()
    sisa = (tanggal - datetime.date.today()).days
    data_store['hitung'].append({
        'acara': request.form['acara'],
        'tanggal': request.form['tanggal'],
        'sisa_hari': max(0, sisa)
    })
    return redirect(url_for('page', page='hitung'))

@app.route('/teks', methods=['POST'])
def handle_teks():
    teks = request.form['teks']
    gaya = request.form['gaya']
    session['styled_text'] = stylize_text(teks, gaya)
    return redirect(url_for('page', page='teks'))

@app.route('/favorit', methods=['POST'])
def handle_favorit():
    data_store['favorit'].append({
        'judul': request.form['judul'],
        'url': request.form['url'],
        'catatan': request.form['catatan']
    })
    return redirect(url_for('page', page='favorit'))

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
    return redirect(url_for('page', page='ketik'))

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
    return redirect(url_for('page', page='konversi'))

# ==========================================
# JALANKAN APLIKASI
# ==========================================
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
