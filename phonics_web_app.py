# phonics_web_app.py - Simplified version with minimal dependencies
import streamlit as st
import sqlite3
import random
import json
from datetime import datetime
import time

# Configure page
st.set_page_config(
    page_title="🌈 Phonics Adventure Kingdom 🏰",
    page_icon="🦄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

class PhonicsWebApp:
    def __init__(self):
        self.init_session_state()
        self.init_database()
        self.init_phonics_data()
        self.load_custom_css()

    def init_session_state(self):
        """Initialize Streamlit session state"""
        if 'current_screen' not in st.session_state:
            st.session_state.current_screen = 'splash'
        if 'current_user' not in st.session_state:
            st.session_state.current_user = None
        if 'current_theme' not in st.session_state:
            st.session_state.current_theme = 'rainbow'
        if 'score' not in st.session_state:
            st.session_state.score = 0
        if 'current_letter' not in st.session_state:
            st.session_state.current_letter = 'A'
        if 'activity_start_time' not in st.session_state:
            st.session_state.activity_start_time = time.time()
        if 'show_celebration' not in st.session_state:
            st.session_state.show_celebration = False
        if 'splash_complete' not in st.session_state:
            st.session_state.splash_complete = False

    def init_database(self):
        """Initialize SQLite database"""
        self.conn = sqlite3.connect('phonics_kids_web.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        
        # Create tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                created_date TEXT,
                total_points INTEGER DEFAULT 0,
                level TEXT DEFAULT 'beginner',
                theme TEXT DEFAULT 'rainbow',
                total_stars INTEGER DEFAULT 0,
                favorite_activity TEXT DEFAULT 'letter_sounds'
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                activity TEXT,
                content TEXT,
                score INTEGER,
                time_spent INTEGER,
                date TEXT,
                stars_earned INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        self.conn.commit()

    def init_phonics_data(self):
        """Initialize all phonics data from original app"""
        self.themes = {
            'rainbow': {
                'bg': '#FFB6C1', 'primary': '#FF69B4', 'secondary': '#98FB98',
                'accent': '#FFD700', 'text': '#FFFFFF', 'button': '#FF1493'
            },
            'ocean': {
                'bg': '#87CEEB', 'primary': '#00CED1', 'secondary': '#B0E0E6',
                'accent': '#FF6347', 'text': '#FFFFFF', 'button': '#1E90FF'
            },
            'forest': {
                'bg': '#98FB98', 'primary': '#32CD32', 'secondary': '#90EE90',
                'accent': '#FFD700', 'text': '#FFFFFF', 'button': '#228B22'
            },
            'space': {
                'bg': '#9370DB', 'primary': '#8A2BE2', 'secondary': '#DDA0DD',
                'accent': '#FFD700', 'text': '#FFFFFF', 'button': '#4B0082'
            },
            'candy': {
                'bg': '#FFB6C1', 'primary': '#FF69B4', 'secondary': '#FFC0CB',
                'accent': '#98FB98', 'text': '#FFFFFF', 'button': '#DC143C'
            }
        }

        self.letter_sounds = {
            'A': 'ay', 'B': 'buh', 'C': 'kuh', 'D': 'duh', 'E': 'eh',
            'F': 'fuh', 'G': 'guh', 'H': 'huh', 'I': 'ih', 'J': 'juh',
            'K': 'kuh', 'L': 'luh', 'M': 'muh', 'N': 'nuh', 'O': 'oh',
            'P': 'puh', 'Q': 'kwuh', 'R': 'ruh', 'S': 'suh', 'T': 'tuh',
            'U': 'uh', 'V': 'vuh', 'W': 'wuh', 'X': 'ks', 'Y': 'yuh', 'Z': 'zuh'
        }

        self.mascot_messages = [
            "You're doing GREAT! 🌟",
            "Keep up the awesome work! 🎈",
            "I'm so proud of you! 💖",
            "You're a phonics superstar! ⭐",
            "Learning is fun with you! 🦄",
            "Wow! You're amazing! 🎉"
        ]

    def load_custom_css(self):
        """Load custom CSS for kid-friendly styling"""
        theme = self.themes[st.session_state.current_theme]
        
        css = f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@400;700&display=swap');
        
        .stApp {{
            background: linear-gradient(135deg, {theme['bg']}, {theme['secondary']});
            font-family: 'Comic Neue', 'Comic Sans MS', cursive;
        }}
        
        .main-title {{
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            background: linear-gradient(45deg, #FF0000, #FF7F00, #FFFF00, #00FF00, #0000FF, #4B0082, #9400D3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 2rem;
            animation: rainbow 3s ease-in-out infinite alternate;
        }}
        
        .magic-card {{
            background: linear-gradient(135deg, {theme['primary']}, {theme['accent']});
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            border: 3px solid {theme['accent']};
            text-align: center;
            transition: transform 0.3s ease;
            margin: 1rem;
        }}
        
        .magic-card:hover {{
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 12px 40px rgba(0,0,0,0.4);
        }}
        
        .letter-bubble {{
            background: linear-gradient(135deg, #FFD700, #FFA500);
            border-radius: 50%;
            width: 200px;
            height: 200px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 2rem auto;
            box-shadow: 0 8px 32px rgba(255,215,0,0.5);
            animation: float 3s ease-in-out infinite;
        }}
        
        .letter-text {{
            font-size: 6rem;
            font-weight: bold;
            color: {theme['button']};
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .celebration {{
            animation: celebrate 1s ease-in-out;
        }}
        
        .score-display {{
            background: linear-gradient(135deg, {theme['accent']}, {theme['primary']});
            color: white;
            padding: 1rem 2rem;
            border-radius: 25px;
            font-size: 1.5rem;
            font-weight: bold;
            text-align: center;
            box-shadow: 0 4px 16px rgba(0,0,0,0.3);
            margin: 1rem;
        }}
        
        .mascot-speech {{
            background: white;
            border: 3px solid {theme['primary']};
            border-radius: 20px;
            padding: 1rem;
            position: relative;
            box-shadow: 0 4px 16px rgba(0,0,0,0.2);
            margin: 1rem;
        }}
        
        @keyframes rainbow {{
            0% {{ filter: hue-rotate(0deg); }}
            100% {{ filter: hue-rotate(360deg); }}
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-20px); }}
        }}
        
        @keyframes celebrate {{
            0% {{ transform: scale(1) rotate(0deg); }}
            25% {{ transform: scale(1.1) rotate(5deg); }}
            50% {{ transform: scale(1.2) rotate(-5deg); }}
            75% {{ transform: scale(1.1) rotate(5deg); }}
            100% {{ transform: scale(1) rotate(0deg); }}
        }}
        
        .stButton > button {{
            background: linear-gradient(135deg, {theme['button']}, {theme['primary']});
            color: white;
            border: none;
            border-radius: 25px;
            padding: 0.75rem 2rem;
            font-size: 1.2rem;
            font-weight: bold;
            font-family: 'Comic Neue', cursive;
            box-shadow: 0 4px 16px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        }}
        </style>
        """
        
        st.markdown(css, unsafe_allow_html=True)

    def show_splash_screen(self):
        """Magical splash screen"""
        st.markdown('<div style="text-align: center; padding: 4rem 2rem;">', unsafe_allow_html=True)
        st.markdown('<h1 class="main-title">🌈 PHONICS ADVENTURE KINGDOM 🏰</h1>', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align: center; color: #FF1493; font-size: 1.8rem;">✨ Where Learning is Pure Magic! ✨</h2>', unsafe_allow_html=True)
        
        # Animated loading
        if not st.session_state.splash_complete:
            with st.empty():
                for i in range(4):
                    if i == 0:
                        st.markdown('<p style="text-align: center; font-size: 1.3rem;">🌟 Loading magical adventures... 🌟</p>', unsafe_allow_html=True)
                    elif i == 1:
                        st.markdown('<p style="text-align: center; font-size: 1.3rem;">🦄 Preparing your kingdom... 🦄</p>', unsafe_allow_html=True)
                    elif i == 2:
                        st.markdown('<p style="text-align: center; font-size: 1.3rem;">✨ Almost ready for magic! ✨</p>', unsafe_allow_html=True)
                    else:
                        st.markdown('<p style="text-align: center; font-size: 2rem; margin: 2rem 0;">⭐ ✨ 🌟 ✨ ⭐</p>', unsafe_allow_html=True)
                    time.sleep(1)
            
            st.session_state.splash_complete = True
            st.rerun()
        
        if st.button("🚀 Enter the Kingdom! 🚀", key="enter_kingdom"):
            st.session_state.current_screen = 'user_selection'
            st.rerun()

    def show_user_selection(self):
        """User selection with theme chooser"""
        st.markdown('<h1 class="main-title">🌟 Welcome to the Magic Kingdom! 🌟</h1>', unsafe_allow_html=True)
        
        # Theme selector
        st.markdown('<h3 style="text-align: center; color: #FF1493;">🎨 Choose Your Magical Theme! 🎨</h3>', unsafe_allow_html=True)
        
        theme_cols = st.columns(5)
        theme_info = {
            'rainbow': ('🌈 Rainbow Magic', '#FF69B4'),
            'ocean': ('🌊 Ocean Adventure', '#1E90FF'), 
            'forest': ('🌲 Forest Friends', '#228B22'),
            'space': ('🚀 Space Explorer', '#4B0082'),
            'candy': ('🍭 Candy Kingdom', '#DC143C')
        }
        
        for i, (theme_name, (display_name, color)) in enumerate(theme_info.items()):
            with theme_cols[i]:
                if st.button(display_name, key=f"theme_{theme_name}"):
                    st.session_state.current_theme = theme_name
                    st.rerun()

        st.markdown("---")
        
        # User selection columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="magic-card">', unsafe_allow_html=True)
            st.markdown('<h3>🏰 Choose Your Character</h3>', unsafe_allow_html=True)
            
            # Get existing users
            try:
                self.cursor.execute("SELECT name, total_points, level, total_stars FROM users ORDER BY total_points DESC")
                users = self.cursor.fetchall()
                
                if users:
                    for user in users[:5]:  # Show top 5 users
                        user_name, points, level, stars = user
                        if st.button(f"🦄 {user_name} - 🏆{points} ⭐{stars} 🎯{level.title()}", 
                                   key=f"user_{user_name}"):
                            st.session_state.current_user = user_name
                            st.session_state.current_screen = 'main_menu'
                            st.rerun()
                else:
                    st.info("No existing characters found. Create your first character!")
                    
            except Exception as e:
                st.error(f"Database error: {e}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="magic-card">', unsafe_allow_html=True)
            st.markdown('<h3>✨ Create New Character</h3>', unsafe_allow_html=True)
            
            # Character creation
            st.markdown("🌟 Choose your magical friend:")
            magical_friends = ['🦄 Unicorn', '🐉 Dragon', '🧚 Fairy', '🧙 Wizard', '👸 Princess', '🤴 Knight']
            
            selected_mascot = st.selectbox("", magical_friends, key="mascot_select")
            
            st.markdown("🌟 What's your magical name?")
            new_user_name = st.text_input("", placeholder="Enter your magical name...", key="new_user_input")
            
            if st.button("🚀 Start My Adventure!", key="create_user"):
                if new_user_name.strip():
                    if self.create_new_user(new_user_name.strip()):
                        st.session_state.current_user = new_user_name.strip()
                        st.session_state.current_screen = 'welcome'
                        st.rerun()
                else:
                    st.error("Please enter your magical name!")
            
            st.markdown('</div>', unsafe_allow_html=True)

    def create_new_user(self, name):
        """Create new user in database"""
        try:
            self.cursor.execute(
                "INSERT INTO users (name, created_date, theme, favorite_activity) VALUES (?, ?, ?, ?)",
                (name, datetime.now().isoformat(), st.session_state.current_theme, 'letter_sounds')
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            st.error("This magical name already exists! Try a different one!")
            return False
        except Exception as e:
            st.error(f"Something magical went wrong: {e}")
            return False

    def show_welcome_screen(self):
        """Welcome new user"""
        st.markdown('<div style="text-align: center; padding: 4rem 2rem;">', unsafe_allow_html=True)
        st.markdown('<h1 style="text-align: center; color: #FF1493;">🎊 Welcome to the Adventure! 🎊</h1>', unsafe_allow_html=True)
        st.markdown(f'<h2 style="text-align: center; color: #4B0082;">Hello, {st.session_state.current_user}! 🦄</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; font-size: 1.3rem; color: #FF1493; margin: 2rem 0;">
        Get ready for magical learning adventures!<br>
        You'll earn stars, unlock achievements,<br>
        and have tons of fun!
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<p style="text-align: center; font-size: 2.5rem;">⭐ ✨ 🌟 ✨ ⭐</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🎮 Let's Start Learning! 🎮", key="start_learning"):
            st.session_state.current_screen = 'main_menu'
            st.rerun()

    def show_main_menu(self):
        """Main menu with activities"""
        # Header with user info
        try:
            self.cursor.execute("SELECT total_points, total_stars, level FROM users WHERE name = ?", 
                              (st.session_state.current_user,))
            result = self.cursor.fetchone()
            if result:
                points, stars, level = result
            else:
                points, stars, level = 0, 0, 'beginner'
        except:
            points, stars, level = 0, 0, 'beginner'

        # Header
        st.markdown(f'<h1 class="main-title">🌟 Welcome back, {st.session_state.current_user}! 🌟</h1>', unsafe_allow_html=True)
        
        # Stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="score-display">🏆 Points: {points}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="score-display">⭐ Stars: {stars}</div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="score-display">🎯 Level: {level.title()}</div>', unsafe_allow_html=True)
        with col4:
            if st.button("🚪 Switch Character", key="logout"):
                st.session_state.current_user = None
                st.session_state.current_screen = 'user_selection'
                st.rerun()

        st.markdown('<h2 style="text-align: center; color: #FF1493; margin: 2rem 0;">🎮 Choose Your Learning Adventure! 🎮</h2>', unsafe_allow_html=True)
        
        # Activity grid - Letter Sounds (working) and placeholders
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="magic-card" style="background: linear-gradient(135deg, #FF69B4, {self.themes[st.session_state.current_theme]['accent']});">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🔤</div>
                <h3 style="color: white; margin-bottom: 1rem;">Letter Magic</h3>
                <p style="color: white; margin-bottom: 1.5rem;">Learn magical letter sounds!</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Play Letter Magic!", key="activity_letter_sounds"):
                st.session_state.current_screen = 'letter_sounds'
                st.session_state.activity_start_time = time.time()
                st.session_state.score = 0
                st.rerun()
        
        with col2:
            st.markdown(f"""
            <div class="magic-card" style="background: linear-gradient(135deg, #FFD700, {self.themes[st.session_state.current_theme]['accent']});">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🔨</div>
                <h3 style="color: white; margin-bottom: 1rem;">Word Wizard</h3>
                <p style="color: white; margin-bottom: 1.5rem;">Blend sounds like magic!</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Play Word Wizard!", key="activity_word_wizard"):
                st.info("Word Wizard adventure coming soon! 🌟")
        
        with col3:
            st.markdown(f"""
            <div class="magic-card" style="background: linear-gradient(135deg, #32CD32, {self.themes[st.session_state.current_theme]['accent']});">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🏗️</div>
                <h3 style="color: white; margin-bottom: 1rem;">Word Builder</h3>
                <p style="color: white; margin-bottom: 1.5rem;">Build amazing words!</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Play Word Builder!", key="activity_word_builder"):
                st.info("Word Builder quest coming soon! 🌟")

        # Mascot in sidebar
        with st.sidebar:
            st.markdown('<div style="text-align: center; font-size: 4rem;">🦄</div>', unsafe_allow_html=True)
            message = random.choice(self.mascot_messages)
            st.markdown(f'<div class="mascot-speech">{message}</div>', unsafe_allow_html=True)

    def show_letter_sounds_activity(self):
        """Letter sounds activity"""
        theme = self.themes[st.session_state.current_theme]
        
        # Header
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {theme['primary']}, {theme['accent']}); 
                    padding: 2rem; border-radius: 15px; text-align: center; margin-bottom: 2rem;">
            <h1 style="color: white; margin: 0;">🔤 Letter Magic Adventure! 🔤</h1>
        </div>
        """, unsafe_allow_html=True)

        # Score display
        st.markdown(f'<div class="score-display">⭐ Stars: {st.session_state.score}</div>', unsafe_allow_html=True)

        # Letter display
        if 'current_letter' not in st.session_state:
            st.session_state.current_letter = random.choice(list(self.letter_sounds.keys()))
        
        current_sound = self.letter_sounds[st.session_state.current_letter]
        
        # Show celebration if triggered
        celebration_class = "celebration" if st.session_state.show_celebration else ""
        
        st.markdown(f"""
        <div class="letter-bubble {celebration_class}">
            <div class="letter-text">{st.session_state.current_letter}</div>
        </div>
        """, unsafe_allow_html=True)

        # Sound information
        st.markdown(f'<h2 style="text-align: center; color: {theme["button"]}; margin: 2rem 0;">✨ This letter says: {current_sound} ✨</h2>', unsafe_allow_html=True)

        # Control buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("🔊 Hear the Magic Sound!", key="speak_letter"):
                self.speak_letter_sound()
            
            if st.button("➡️ Next Letter Adventure!", key="next_letter"):
                st.session_state.current_letter = random.choice(list(self.letter_sounds.keys()))
                st.rerun()

        # Back button
        if st.button("🏠 Back to Adventure Map", key="back_to_menu"):
            st.session_state.current_screen = 'main_menu'
            st.rerun()

        # Reset celebration state
        if st.session_state.show_celebration:
            st.session_state.show_celebration = False

    def speak_letter_sound(self):
        """Handle letter sound with celebration"""
        # Update score
        st.session_state.score += 5
        
        # Trigger celebration
        st.session_state.show_celebration = True
        
        # Save progress
        self.save_activity_progress("letter_sounds", st.session_state.current_letter, 5)
        
        # Show success message
        st.success("⭐ Great Job! Awesome listening! You earned a star! ⭐")
        
        # Text-to-speech simulation (you can integrate real TTS here)
        sound = self.letter_sounds[st.session_state.current_letter]
        st.info(f"🔊 Speaking: The letter {st.session_state.current_letter} says {sound}!")

    def save_activity_progress(self, activity, content, score):
        """Save user progress to database"""
        if st.session_state.current_user:
            try:
                # Get user ID
                self.cursor.execute("SELECT id FROM users WHERE name = ?", (st.session_state.current_user,))
                result = self.cursor.fetchone()
                
                if result:
                    user_id = result[0]
                    time_spent = int(time.time() - st.session_state.activity_start_time)
                    stars_earned = max(1, score // 5)
                    
                    # Save progress
                    self.cursor.execute("""
                        INSERT INTO progress (user_id, activity, content, score, time_spent, date, stars_earned)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (user_id, activity, content, score, time_spent, datetime.now().isoformat(), stars_earned))
                    
                    # Update user totals
                    self.cursor.execute(
                        "UPDATE users SET total_points = total_points + ?, total_stars = total_stars + ? WHERE id = ?",
                        (score, stars_earned, user_id)
                    )
                    
                    self.conn.commit()
                    
            except Exception as e:
                st.error(f"Error saving progress: {e}")

    def run(self):
        """Main application runner"""
        # Load CSS for current theme
        self.load_custom_css()
        
        # Route to appropriate screen
        if st.session_state.current_screen == 'splash':
            self.show_splash_screen()
        elif st.session_state.current_screen == 'user_selection':
            self.show_user_selection()
        elif st.session_state.current_screen == 'welcome':
            self.show_welcome_screen()
        elif st.session_state.current_screen == 'main_menu':
            self.show_main_menu()
        elif st.session_state.current_screen == 'letter_sounds':
            self.show_letter_sounds_activity()

# Run the application
if __name__ == "__main__":
    app = PhonicsWebApp()
    app.run()
