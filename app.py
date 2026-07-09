# ==========================================
# PROJECT: NEXUS UTILITY SUITE 
# FILE: app.py
# VERSION: PREMIUM v3.0
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
app.secret_key = 'nexus-premium-secret-key-2024'

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
# TEMPLATE UTAMA (DENGAN NAVIGASI PAGE)
# ==========================================
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXUS • Utility Suite Premium</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;600;700&display=swap');
        
        * { 
            font-family: 'Inter', sans-serif;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background: #0a0a12;
            min-height: 100vh;
            color: #e8e8ff;
            overflow-x: hidden;
        }
        
        /* Background Animasi */
        .bg-nexus {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 50%, rgba(120, 80, 255, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 80% 50%, rgba(255, 80, 200, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 50% 100%, rgba(168, 85, 247, 0.05) 0%, transparent 50%);
            z-index: 0;
            animation: pulseBg 10s ease-in-out infinite alternate;
        }
        
        @keyframes pulseBg {
            0% { opacity: 0.6; transform: scale(1); }
            100% { opacity: 1; transform: scale(1.05); }
        }
        
        /* Glassmorphism Premium */
        .glass-premium {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.06);
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        }
        
        .glass-card {
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.06);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        
        .glass-card:hover {
            transform: translateY(-4px);
            border-color: rgba(168, 85, 247, 0.25);
            box-shadow: 0 12px 40px rgba(168, 85, 247, 0.1);
        }
        
        /* Gradient Text */
        .gradient-nexus {
            background: linear-gradient(135deg, #a855f7 0%, #ec4899 50%, #f472b6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* Gradient Button */
        .btn-gradient {
            background: linear-gradient(135deg, #7c3aed, #db2777);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .btn-gradient:hover {
            transform: scale(1.03);
            box-shadow: 0 0 30px rgba(168, 85, 247, 0.3);
        }
        
        /* Input Styling */
        .input-nexus {
            background: rgba(0,0,0,0.4);
            border: 1px solid rgba(255,255,255,0.08);
            color: #e8e8ff;
            transition: all 0.3s ease;
            border-radius: 12px;
            padding: 12px 16px;
            width: 100%;
        }
        
        .input-nexus:focus {
            border-color: #a855f7;
            box-shadow: 0 0 0 4px rgba(168, 85, 247, 0.15);
            outline: none;
            background: rgba(0,0,0,0.6);
        }
        
        .input-nexus::placeholder {
            color: rgba(255,255,255,0.3);
        }
        
        /* ==========================================
           MENU NAVIGASI PREMIUM (PAGE-BASED)
           ========================================== */
        .menu-container {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 10px;
            padding: 8px;
        }
        
        @media (max-width: 640px) {
            .menu-container {
                grid-template-columns: repeat(4, 1fr);
                gap: 8px;
                padding: 4px;
            }
        }
        
        @media (max-width: 400px) {
            .menu-container {
                grid-template-columns: repeat(3, 1fr);
                gap: 6px;
            }
        }
        
        .menu-item {
            background: rgba(255, 255, 255, 0.03);
            border: 2px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 14px 8px;
            text-align: center;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            cursor: pointer;
            text-decoration: none;
            color: #a0a0c0;
            position: relative;
            overflow: hidden;
        }
        
        .menu-item::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(168, 85, 247, 0.1), transparent);
            transition: all 0.5s ease;
        }
        
        .menu-item:hover::before {
            left: 100%;
        }
        
        .menu-item:hover {
            transform: translateY(-4px) scale(1.03);
            border-color: rgba(168, 85, 247, 0.3);
            background: rgba(168, 85, 247, 0.08);
            box-shadow: 0 8px 25px rgba(168, 85, 247, 0.15);
            color: #e8e8ff;
        }
        
        .menu-item.active {
            border-color: #a855f7;
            background: rgba(168, 85, 247, 0.12);
            box-shadow: 0 0 30px rgba(168, 85, 247, 0.1);
            color: #ffffff;
        }
        
        .menu-item.active .menu-icon {
            transform: scale(1.1);
        }
        
        .menu-icon {
            font-size: 1.8rem;
            display: block;
            margin-bottom: 4px;
            transition: transform 0.3s ease;
        }
        
        .menu-label {
            font-size: 0.65rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        
        @media (max-width: 640px) {
            .menu-icon { font-size: 1.4rem; }
            .menu-label { font-size: 0.55rem; }
            .menu-item { padding: 10px 4px; }
        }
        
        /* Welcome Screen */
        .welcome-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 9999;
            background: #0a0a12;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: fadeIn 0.8s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.95); }
            to { opacity: 1; transform: scale(1); }
        }
        
        .welcome-content {
            text-align: center;
            animation: floatGlow 4s ease-in-out infinite;
        }
        
        @keyframes floatGlow {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-12px); }
        }
        
        .nexus-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 4.5rem;
            font-weight: 900;
            background: linear-gradient(135deg, #a855f7, #ec4899, #f472b6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 60px rgba(168, 85, 247, 0.3);
            letter-spacing: 6px;
        }
        
        @media (max-width: 640px) {
            .nexus-title { font-size: 2.8rem; letter-spacing: 3px; }
        }
        
        .sub-glow {
            color: #8080aa;
            font-weight: 300;
            letter-spacing: 10px;
            text-transform: uppercase;
            font-size: 0.9rem;
        }
        
        .btn-enter {
            background: linear-gradient(135deg, #7c3aed, #db2777);
            padding: 16px 48px;
            border-radius: 50px;
            color: white;
            font-weight: 700;
            font-size: 1.1rem;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 0 30px rgba(168, 85, 247, 0.2);
            letter-spacing: 3px;
        }
        
        .btn-enter:hover {
            transform: scale(1.05);
            box-shadow: 0 0 50px rgba(168, 85, 247, 0.4);
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: rgba(255,255,255,0.02); }
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #7c3aed, #db2777);
            border-radius: 10px;
        }
        
        .fade-slide {
            animation: fadeSlide 0.6s ease forwards;
        }
        
        @keyframes fadeSlide {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Badge notifikasi */
        .badge-count {
            background: linear-gradient(135deg, #ec4899, #a855f7);
            color: white;
            font-size: 0.6rem;
            padding: 2px 8px;
            border-radius: 20px;
            margin-left: 4px;
        }
    </style>
</head>
<body>
    <!-- Background -->
    <div class="bg-nexus"></div>

    <!-- WELCOME SCREEN -->
    <div id="welcomeScreen" class="welcome-screen">
        <div class="welcome-content px-6">
            <div class="text-7xl mb-4">🚀</div>
            <h1 class="nexus-title">NEXUS</h1>
            <p class="sub-glow mb-6">Utility Suite • Premium</p>
            <p class="text-gray-400 mb-8 max-w-md mx-auto text-sm">
                Pusat kendali 10 fitur canggih dalam satu platform
            </p>
            <button onclick="enterNexus()" class="btn-enter">
                ✦ LANJUTKAN ✦
            </button>
            <p class="text-gray-600 text-xs mt-4">v3.0 • Made with ❤️</p>
        </div>
    </div>

    <!-- MAIN CONTENT -->
    <div id="mainContent" style="display: none;" class="relative z-10 p-4 md:p-6">
        <div class="max-w-6xl mx-auto">
            <!-- HEADER -->
            <header class="text-center py-6 fade-slide">
                <h1 class="text-3xl md:text-5xl font-bold gradient-nexus font-['Orbitron'] tracking-wider">
                    ⚡ NEXUS
                </h1>
                <p class="text-gray-400 text-sm md:text-base tracking-widest mt-1">10 Fitur Premium • Satu Platform</p>
            </header>

            <!-- MENU NAVIGASI (PAGE-BASED) -->
            <nav class="glass-premium rounded-2xl p-4 md:p-6 mb-8 fade-slide">
                <div class="menu-container">
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
                           class="menu-item {% if active == id %}active{% endif %}"
                           onclick="setActive('{{ id }}')">
                            <span class="menu-icon">{{ icon }}</span>
                            <span class="menu-label">{{ label }}</span>
                        </a>
                    {% endfor %}
                </div>
            </nav>

            <!-- KONTEN FITUR -->
            <div class="fade-slide">
                {% block content %}{% endblock %}
            </div>

            <!-- FOOTER -->
            <footer class="text-center text-gray-600 text-xs py-8 mt-12 border-t border-purple-900/20">
                NEXUS Utility Suite • Data tersimpan di memori • Made with ❤️
            </footer>
        </div>
    </div>

    <script>
        // Welcome Screen
        function enterNexus() {
            const welcome = document.getElementById('welcomeScreen');
            const main = document.getElementById('mainContent');
            welcome.style.opacity = '0';
            welcome.style.transition = 'opacity 0.8s ease';
            setTimeout(() => {
                welcome.style.display = 'none';
                main.style.display = 'block';
                main.style.animation = 'fadeSlide 0.8s ease';
            }, 800);
        }

        // Set Active Menu (highlight)
        function setActive(id) {
            document.querySelectorAll('.menu-item').forEach(el => el.classList.remove('active'));
            const activeEl = document.querySelector(`.menu-item[href="/${id}"]`);
            if(activeEl) activeEl.classList.add('active');
        }

        // Auto detect active from URL
        document.addEventListener('DOMContentLoaded', function() {
            const path = window.location.pathname;
            const activeId = path.replace('/', '') || 'ucapan';
            setActive(activeId);
        });
    </script>
</body>
</html>
"""

# ==========================================
# ROUTE UNTUK SETIAP HALAMAN (PAGE-BASED)
# ==========================================
@app.route('/')
def index():
    return redirect(url_for('page', page='ucapan'))

@app.route('/<page>')
def page(page):
    # Validasi page
    valid_pages = ['ucapan', 'pesan', 'kuis', 'qr', 'keuangan', 'hitung', 'teks', 'favorit', 'ketik', 'konversi']
    if page not in valid_pages:
        page = 'ucapan'
    
    contents = {
        'ucapan': """
        <section class="glass-card rounded-2xl p-6 md:p-8">
            <div class="flex items-center gap-3 mb-6">
                <span class="text-3xl">🎉</span>
                <h2 class="text-2xl font-bold gradient-nexus">Pembuat Kartu Ucapan & Undangan</h2>
            </div>
            <form method="POST" action="/ucapan" class="space-y-4">
                <input type="text" name="nama" placeholder="Nama penerima" class="input-nexus" required>
                <input type="text" name="acara" placeholder="Jenis acara" class="input-nexus" required>
                <textarea name="pesan" rows="3" placeholder="Pesan ucapan..." class="input-nexus" required></textarea>
                <button type="submit" class="btn-gradient w-full py-3 rounded-xl font-semibold text-white">✨ Buat Kartu</button>
            </form>
            <div class="mt-6 space-y-4">
                {% for item in store.ucapan %}
                <div class="glass-card p-4 rounded-xl border border-purple-500/20">
                    <p class="font-semibold text-purple-300">Untuk: {{ item.nama }}</p>
                    <p class="text-pink-300">Acara: {{ item.acara }}</p>
                    <p class="text-gray-300 italic">"{{ item.pesan }}"</p>
                    <small class="text-gray-500">{{ item.waktu }}</small>
                </div>
                {% endfor %}
            </div>
        </section>
        """,
        'pesan': """
        <section class="glass-card rounded-2xl p-6 md:p-8">
            <div class="flex items-center gap-3 mb-6">
                <span class="text-3xl">💌</span>
                <h2 class="text-2xl font-bold gradient-nexus">Kotak Pesan Rahasia Anonim</h2>
            </div>
            <form method="POST" action="/pesan" class="space-y-4">
                <input type="text" name="judul" placeholder="Judul (opsional)" class="input-nexus">
                <textarea name="isi" rows="4" placeholder="Tulis pesan rahasia..." class="input-nexus" required></textarea>
                <button type="submit" class="btn-gradient w-full py-3 rounded-xl font-semibold text-white">🤫 Kirim Rahasia</button>
            </form>
            <div class="mt-6 space-y-4">
                {% for item in store.pesan %}
                <div class="glass-card p-4 rounded-xl border border-pink-500/20">
                    <p class="text-gray-300">{{ item.isi }}</p>
                    <small class="text-gray-500">#{{ item.id }} • {{ item.waktu }}</small>
                </div>
                {% endfor %}
            </div>
        </section>
        """,
        'kuis': """
        <section class="glass-card rounded-2xl p-6 md:p-8">
            <div class="flex items-center gap-3 mb-6">
                <span class="text-3xl">🧠</span>
                <h2 class="text-2xl font-bold gradient-nexus">Kuis "Seberapa Kenal Kamu?"</h2>
            </div>
            <form method="POST" action="/kuis" class="space-y-4">
                <div class="glass-card p-4 rounded-xl border border-purple-500/20">
                    <p class="text-gray-300">Pertanyaan: Apa makanan favorit saya?</p>
                </div>
                <input type="text" name="jawaban" placeholder="Jawaban..." class="input-nexus" required>
                <button type="submit" class="btn-gradient w-full py-3 rounded-xl font-semibold text-white">Kirim Jawaban</button>
            </form>
            <div class="mt-6">
                <p class="text-gray-400">Skor Anda: <span class="text-purple-300 font-bold text-2xl">{{ session.get('skor_kuis', 0) }}</span></p>
                {% if session.get('last_answer') %}
                <div class="glass-card p-4 rounded-xl mt-3 border border-purple-500/20">
                    <p class="text-gray-300">{{ session.get('last_answer') }}</p>
                </div>
                {% endif %}
            </div>
        </section>
        """,
        'qr': """
        <section class="glass-card rounded-2xl p-6 md:p-8">
            <div class="flex items-center gap-3 mb-6">
                <span class="text-3xl">📱</span>
                <h2 class="text-2xl font-bold gradient-nexus">Pembuat QR & Pemendek Tautan</h2>
            </div>
            <form method="POST" action="/qr" class="space-y-4">
                <input type="url" name="url" placeholder="Masukkan URL..." class="input-nexus" required>
                <button type="submit" class="btn-gradient w-full py-3 rounded-xl font-semibold text-white">🔗 Buat QR</button>
            </form>
            {% if session.get('qr_result') %}
            <div class="mt-6 glass-card p-4 rounded-xl border border-purple-500/20 text-center">
                <p class="text-gray-300 break-all">Short URL: <a href="{{ session.qr_result.short }}" target="_blank" class="text-purple-300 hover:underline">{{ session.qr_result.short }}</a></p>
                <img src="data:image/png;base64,{{ session.qr_result.qr }}" class="mx-auto mt-3 w-48 h-48" alt="QR Code">
            </div>
            {% endif %}
        </section>
        """,
        'keuangan': """
        <section class="glass-card rounded-2xl p-6 md:p-8">
            <div class="flex items-center gap-3 mb-6">
                <span class="text-3xl">💰</span>
                <h2 class="text-2xl font-bold gradient-nexus">Catatan Pengeluaran & Simpanan</h2>
            </div>
            <form method="POST" action="/keuangan" class="space-y-4">
                <select name="jenis" class="input-nexus">
                    <option value="pengeluaran">Pengeluaran</option>
                    <option value="simpanan">Simpanan</option>
                </select>
                <input type="number" name="jumlah" placeholder="Jumlah (Rp)" class="input-nexus" required>
                <input type="text" name="keterangan" placeholder="Keterangan" class="input-nexus">
                <button type="submit" class="btn-gradient w-full py-3 rounded-xl font-semibold text-white">Tambah Catatan</button>
            </form>
            <div class="mt-6">
                <div class="grid grid-cols-2 gap-4 mb-4">
                    <div class="glass-card p-4 rounded-xl text-center">
                        <p class="text-gray-400 text-sm">Total Pengeluaran</p>
                        <p class="text-2xl font-bold text-pink-400">Rp {{ "%.0f"|format(store.keuangan|selectattr('jenis', 'eq', 'pengeluaran')|map(attribute='jumlah')|sum) }}</p>
                    </div>
                    <div class="glass-card p-4 rounded-xl text-center">
                        <p class="text-gray-400 text-sm">Total Simpanan</p>
                        <p class="text-2xl font-bold text-purple-400">Rp {{ "%.0f"|format(store.keuangan|selectattr('jenis', 'eq', 'simpanan')|map(attribute='jumlah')|sum) }}</p>
                    </div>
                </div>
                <div class="space-y-2 max-h-60 overflow-y-auto">
                    {% for item in store.keuangan[-10:]|reverse %}
                    <div class="glass-card p-3 rounded-xl text-sm flex justify-between items-center">
                        <span>{{ item.jenis }} • {{ item.keterangan }}</span>
                        <span class="font-bold {% if item.jenis == 'pengeluaran' %}text-pink-400{% else %}text-purple-400{% endif %}">Rp {{ "%.0f"|format(item.jumlah) }}</span>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </section>
        """,
        'hitung': """
        <section class="glass-card rounded-2xl p-6 md:p-8">
            <div class="flex items-center gap-3 mb-6">
                <span class="text-3xl">⏳</span>
                <h2 class="text-2xl font-bold gradient-nexus">Penghitung Sisa Hari</h2>
            </div>
            <form method="POST" action="/hitung" class="space-y-4">
                <input type="text" name="acara" placeholder="Nama acara" class="input-nexus" required>
                <input type="date" name="tanggal" class="input-nexus" required>
                <button type="submit" class="btn-gradient w-full py-3 rounded-xl font-semibold text-white">⏱️ Hitung Hari</button>
            </form>
            <div class="mt-6 space-y-4">
                {% for item in store.hitung %}
                <div class="glass-card p-4 rounded-xl border border-purple-500/20">
                    <p class="font-semibold">{{ item.acara }}</p>
                    <p class="text-3xl font-bold text-purple-300">{{ item.sisa_hari }} hari lagi</p>
                    <small class="text-gray-500">{{ item.tanggal }}</small>
                </div>
                {% endfor %}
            </div>
        </section>
        """,
        'teks': """
        <section class="glass-card rounded-2xl p-6 md:p-8">
            <div class="flex items-center gap-3 mb-6">
                <span class="text-3xl">✨</span>
                <h2 class="text-2xl font-bold gradient-nexus">Pengubah Teks Gaya Unik</h2>
            </div>
            <form method="POST" action="/teks" class="space-y-4">
                <input type="text" name="teks" placeholder="Masukkan teks..." class="input-nexus" required>
                <select name="gaya" class="input-nexus">
                    <option value="esthetic">Estetik (𝓪𝓫𝓬)</option>
                    <option value="upside">Terbalik (ɐqɔ)</option>
                </select>
                <button type="submit" class="btn-gradient w-full py-3 rounded-xl font-semibold text-white">✨ Ubah Gaya</button>
            </form>
            {% if session.get('styled_text') %}
            <div class="mt-6 glass-card p-4 rounded-xl border border-purple-500/20 text-center">
                <p class="text-2xl">{{ session.styled_text }}</p>
            </div>
            {% endif %}
        </section>
        """,
        'favorit': """
        <section class="glass-card rounded-2xl p-6 md:p-8">
            <div class="flex items-center gap-3 mb-6">
                <span class="text-3xl">⭐</span>
                <h2 class="text-2xl font-bold gradient-nexus">Penyimpanan Favorit & Bacaan Nanti</h2>
            </div>
            <form method="POST" action="/favorit" class="space-y-4">
                <input type="text" name="judul" placeholder="Judul" class="input-nexus" required>
                <input type="url" name="url" placeholder="URL (opsional)" class="input-nexus">
                <textarea name="catatan" rows="2" placeholder="Catatan..." class="input-nexus"></textarea>
                <button type="submit" class="btn-gradient w-full py-3 rounded-xl font-semibold text-white">⭐ Simpan</button>
            </form>
            <div class="mt-6 space-y-3">
                {% for item in store.favorit %}
                <div class="glass-card p-4 rounded-xl border border-purple-500/20">
                    <p class="font-semibold">{{ item.judul }}</p>
                    {% if item.url %}<a href="{{ item.url }}" target="_blank" class="text-purple-300 text-sm hover:underline">{{ item.url }}</a>{% endif %}
                    <p class="text-gray-400 text-sm">{{ item.catatan }}</p>
                </div>
                {% endfor %}
            </div>
        </section>
        """,
        'ketik': """
        <section class="glass-card rounded-2xl p-6 md:p-8">
            <div class="flex items-center gap-3 mb-6">
                <span class="text-3xl">⌨️</span>
                <h2 class="text-2xl font-bold gradient-nexus">Pengecekan Kecepatan Ketik</h2>
            </div>
            <div class="glass-card p-4 rounded-xl mb-4 border border-purple-500/20">
                <p class="text-gray-300 text-sm">Ketik kalimat ini secepat mungkin untuk mengukur kecepatan mengetik Anda.</p>
            </div>
            <form method="POST" action="/ketik" class="space-y-4">
                <input type="text" name="input_ketik" placeholder="Mulai mengetik..." class="input-nexus" required>
                <button type="submit" class="btn-gradient w-full py-3 rounded-xl font-semibold text-white">🚀 Kirim & Hitung</button>
            </form>
            {% if session.get('hasil_ketik') %}
            <div class="mt-6 glass-card p-4 rounded-xl border border-purple-500/20">
                <p class="text-gray-300">Kecepatan: <span class="text-purple-300 font-bold text-xl">{{ session.hasil_ketik }}</span></p>
            </div>
            {% endif %}
        </section>
        """,
        'konversi': """
        <section class="glass-card rounded-2xl p-6 md:p-8">
            <div class="flex items-center gap-3 mb-6">
                <span class="text-3xl">🔄</span>
                <h2 class="text-2xl font-bold gradient-nexus">Konversi Mata Uang & Satuan</h2>
            </div>
            <form method="POST" action="/konversi" class="space-y-4">
                <div class="grid grid-cols-2 gap-3">
                    <input type="number" name="nilai" placeholder="Nilai" class="input-nexus" required>
                    <select name="dari" class="input-nexus">
                        <option value="usd">USD</option>
                        <option value="eur">EUR</option>
                        <option value="idr">IDR</option>
                    </select>
                    <select name="ke" class="input-nexus">
                        <option value="usd">USD</option>
                        <option value="eur">EUR</option>
                        <option value="idr">IDR</option>
                    </select>
                    <select name="jenis_konversi" class="input-nexus">
                        <option value="mata_uang">Mata Uang</option>
                        <option value="panjang">Panjang (m/km)</option>
                        <option value="berat">Berat (kg/g)</option>
                    </select>
                </div>
                <button type="submit" class="btn-gradient w-full py-3 rounded-xl font-semibold text-white">🔄 Konversi</button>
            </form>
            {% if session.get('hasil_konversi') %}
            <div class="mt-6 glass-card p-4 rounded-xl border border-purple-500/20 text-center">
                <p class="text-gray-300">Hasil: <span class="text-purple-300 font-bold text-xl">{{ session.hasil_konversi }}</span></p>
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
