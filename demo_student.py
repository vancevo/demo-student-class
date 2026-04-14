import streamlit as st
import streamlit.components.v1 as components
import random
import base64
import json
from pathlib import Path

# ---------------------------------
# 0. Cấu hình đường dẫn (Hệ thống - Đừng sửa phần này)
# ---------------------------------
ROOT_DIR = Path(__file__).parent

@st.cache_data
def file_to_data_url(path_obj_str):
    path_obj = Path(path_obj_str)
    if not path_obj.exists():
        return ""
    encoded = base64.b64encode(path_obj.read_bytes()).decode("utf-8")
    return "data:audio/mpeg;base64," + encoded

def get_asset_path(relative_path):
    return str(ROOT_DIR / relative_path)

# SOUND URLS FROM LOCAL FILES
BACKGROUND_MUSIC_URL = file_to_data_url(get_asset_path("music/game_theme.mp3"))
ROCK_SOUND_URL       = file_to_data_url(get_asset_path("music/game_click.mp3"))
PAPER_SOUND_URL      = file_to_data_url(get_asset_path("music/game_click.mp3"))
SCISSORS_SOUND_URL   = file_to_data_url(get_asset_path("music/game_click.mp3"))
WIN_SOUND_URL        = file_to_data_url(get_asset_path("music/game_winner.mp3"))
LOSE_SOUND_URL       = file_to_data_url(get_asset_path("music/game_over.mp3"))
TIE_SOUND_URL        = file_to_data_url(get_asset_path("music/game_click.mp3"))

# Image icons (dùng cho giao diện)
IMAGE_PATHS = {
    "Búa": "assets/rock.png",
    "Bao": "assets/paper.png",
    "Kéo": "assets/scissors.png"
}

# ---------------------------------
# 1. Cấu hình trang
# ---------------------------------
st.set_page_config(
    page_title="Học Python: Oẳn Tù Tì (Pro Audio)",
    page_icon="🐢",
    layout="centered"
)

# ---------------------------------
# 2. Khởi tạo bộ nhớ (Session State)
# ---------------------------------
# TODO: Thử thách 1 - Khởi tạo điểm số bằng 0 nếu chưa có
if "player_score" not in st.session_state:
    ### BẮT ĐẦU CODE CỦA EM ###
    pass # Thay dòng này bằng: st.session_state.player_score = 0
    ### KẾT THÚC CODE CỦA EM ###

if "computer_score" not in st.session_state:
    ### BẮT ĐẦU CODE CỦA EM ###
    pass
    ### KẾT THÚC CODE CỦA EM ###

if "player_choice" not in st.session_state:
    st.session_state.player_choice = None

if "computer_choice" not in st.session_state:
    st.session_state.computer_choice = None

if "result_text" not in st.session_state:
    st.session_state.result_text = "Hãy chọn một quân bài!"

if "player_name" not in st.session_state:
    st.session_state.player_name = "Bạn"

# Biến điều khiển âm thanh (Giống demo.py)
if "sound_event_id" not in st.session_state:
    st.session_state.sound_event_id = 0

if "last_choice_sound_key" not in st.session_state:
    st.session_state.last_choice_sound_key = ""

if "last_result_sound_key" not in st.session_state:
    st.session_state.last_result_sound_key = ""

# ---------------------------------
# 3. Helpers & Audio Engine
# ---------------------------------
def set_sound_keys(player_choice, result):
    """Cập nhật các phím âm thanh để hệ thống JavaScript phát nhạc"""
    st.session_state.last_choice_sound_key = player_choice

    if result == "Bạn thắng!":
        st.session_state.last_result_sound_key = "win"
    elif result == "Máy thắng!":
        st.session_state.last_result_sound_key = "lose"
    elif result == "Hòa rồi!":
        st.session_state.last_result_sound_key = "tie"
    else:
        st.session_state.last_result_sound_key = ""

    st.session_state.sound_event_id += 1

def render_audio_engine():
    """Hệ thống phát nhạc bằng JavaScript (Đừng sửa phần này)"""
    payload = {
        "bg": BACKGROUND_MUSIC_URL,
        "Búa": ROCK_SOUND_URL,
        "Bao": PAPER_SOUND_URL,
        "Kéo": SCISSORS_SOUND_URL,
        "win": WIN_SOUND_URL,
        "lose": LOSE_SOUND_URL,
        "tie": TIE_SOUND_URL,
        "eventId": st.session_state.sound_event_id,
        "choiceKey": st.session_state.last_choice_sound_key,
        "resultKey": st.session_state.last_result_sound_key
    }

    html = """
    <script>
    const payload = %s;

    function playOneShot(url, volume) {
        if (!url) return;
        const audio = new Audio(url);
        audio.volume = volume;
        audio.play().catch(() => {});
    }

    function ensureBackgroundMusic(url) {
        if (!url) return;
        let bg = document.getElementById("bg-music-audio");
        if (!bg) {
            bg = document.createElement("audio");
            bg.id = "bg-music-audio";
            bg.loop = true;
            bg.autoplay = true;
            bg.style.display = "none";
            document.body.appendChild(bg);
        }
        if (bg.src !== url) { bg.src = url; }
        bg.volume = 0.35;
        bg.play().catch(() => {});
    }

    ensureBackgroundMusic(payload.bg);

    const storageKey = "tina-rps-last-sound-event-id";
    const lastPlayed = window.localStorage.getItem(storageKey);

    if (String(payload.eventId) !== lastPlayed && payload.eventId > 0) {
        window.localStorage.setItem(storageKey, String(payload.eventId));

        if (payload.choiceKey && payload[payload.choiceKey]) {
            playOneShot(payload[payload.choiceKey], 1.0);
        }

        if (payload.resultKey && payload[payload.resultKey]) {
            setTimeout(() => {
                playOneShot(payload[payload.resultKey], 1.0);
            }, 180);
        }
    }
    </script>
    """ % json.dumps(payload)
    components.html(html, height=0)

# ---------------------------------
# 4. Logic xử lý game - 
##random.choice(choices)
# ---------------------------------
choices = ["Búa", "Bao", "Kéo"]

def play(player_choice):
    st.session_state.player_choice = player_choice

    # TODO: Thử thách 2 - Máy tính chọn bài ngẫu nhiên từ danh sách 'choices'
    ### BẮT ĐẦU CODE CỦA EM ###
    computer_choice = "rock" # Thay "rock" bằng hàm chọn ngẫu nhiên
    ### KẾT THÚC CODE CỦA EM ###
    
    st.session_state.computer_choice = computer_choice
    
    #Hàm này so sánh lựa chọn của người và máy để trả về kết quả:
    #'Bạn thắng!', 'Máy thắng!', hoặc 'Hòa rồi!'
    #"""
    # TODO: Thử thách 3 - Quyết định Thắng, Thua, Hòa bằng if/elif/else
    # Gợi ý: Nếu player_choice == computer_choice thì kết quả là "Hòa rồi!"
    #if, elif, else

    ### BẮT ĐẦU CODE CỦA EM ###
    if player_choice == computer_choice:
        result = ""
    
    st.session_state.result_text = result
    
    ### BẮT ĐẦU CODE CỦA EM (Cộng điểm nếu thắng) ###
    
    # Nếu result == "Bạn thắng!": ...
    if result == "Bạn thắng!":
        st.session_state.player_score = st.session_state.player_score + 1
    elif result == "Máy thắng!":
        st.session_state.computer_score = st.session_state.computer_score + 1
    ### KẾT THÚC CODE CỦA EM ###
    
    # Kích hoạt âm thanh (Giống demo.py)
    set_sound_keys(player_choice, result)

# ---------------------------------
# 5. Giao diện người dùng (UI)
# ---------------------------------
st.title("🐢 Game Oẳn Tù Tì (Thực hành âm thanh)")

# Thông báo mẹo âm thanh
if st.session_state.sound_event_id == 0:
    st.info("💡 Mẹo: Hãy click vào màn hình hoặc chọn nước đi để bắt đầu nghe nhạc nhé!")

st.session_state.player_name = st.text_input(
    "Nhập tên của em:",
    value=st.session_state.player_name
)

# Khởi động hệ thống âm thanh
render_audio_engine()

# Hiển thị điểm số
col_a, col_b = st.columns(2)
col_a.metric(st.session_state.player_name, st.session_state.player_score)
col_b.metric("Máy tính 🤖", st.session_state.computer_score)

st.divider()

# Hiển thị quân bài đã chọn
if st.session_state.player_choice:
    disp1, disp2 = st.columns(2)
    with disp1:
        st.write(f"### {st.session_state.player_name} đã chọn:")
        st.image(str(get_asset_path(IMAGE_PATHS[st.session_state.player_choice])), width=150)
    with disp2:
        st.write("### Máy tính đã chọn:")
        st.image(str(get_asset_path(IMAGE_PATHS[st.session_state.computer_choice])), width=150)

st.divider()

# Các nút chọn
st.subheader("Bấm nút để ra chiêu:")
c1, c2, c3 = st.columns(3)

# TODO: Thử thách 5 - Gọi hàm play() cho từng trường hợp
if c1.button("🔨 Búa", use_container_width=True):
    ### BẮT ĐẦU CODE CỦA EM ###
    play("Búa")
    st.rerun()
    ### KẾT THÚC CODE CỦA EM ###

if c2.button("📄 Bao", use_container_width=True):
    ### BẮT ĐẦU CODE CỦA EM ###
    play("Bao")
    st.rerun()
    ### KẾT THÚC CODE CỦA EM ###

if c3.button("✂️ Kéo", use_container_width=True):
    ### BẮT ĐẦU CODE CỦA EM ###
    play("Kéo")
    st.rerun()
    ### KẾT THÚC CODE CỦA EM ###

st.divider()

# Hiển thị kết quả thắng thua
st.markdown(f"<h2 style='text-align: center;'>{st.session_state.result_text}</h2>", unsafe_allow_html=True)

if st.button("Reset Game"):
    st.session_state.player_score = 0
    st.session_state.computer_score = 0
    st.session_state.result_text = "Hãy chọn một quân bài!"
    st.session_state.player_choice = None
    st.session_state.computer_choice = None
    st.session_state.sound_event_id += 1 # Reset âm thanh
    st.rerun()
