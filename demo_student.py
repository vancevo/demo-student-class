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

# SOUND URLS
SOUNDS = {
    "bg": file_to_data_url(get_asset_path("music/game_theme.mp3")),
    "click": file_to_data_url(get_asset_path("music/game_click.mp3")),
    "win": file_to_data_url(get_asset_path("music/game_winner.mp3")),
    "lose": file_to_data_url(get_asset_path("music/game_over.mp3"))
}

IMAGE_PATHS = {
    "rock":     "assets/rock.png",
    "paper":    "assets/paper.png",
    "scissors": "assets/scissors.png"
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
if "sound_trigger" not in st.session_state:
    st.session_state.sound_trigger = 0
if "last_event" not in st.session_state:
    st.session_state.last_event = ""

# ---------------------------------
# 3. Audio Engine (Dùng bản Simple đã chạy tốt)
# ---------------------------------
def render_audio():
    payload = json.dumps({
        "sounds": SOUNDS,
        "trigger": st.session_state.sound_trigger,
        "event": st.session_state.last_event
    })
    
    html_code = f"""
    <script>
    const data = {payload};
    function playSound(url) {{
        if (!url) return;
        const audio = new Audio(url);
        audio.play().catch(() => {{}});
    }}
    if (!window.bgMusic) {{
        window.bgMusic = new Audio(data.sounds.bg);
        window.bgMusic.loop = true;
        window.bgMusic.volume = 0.3;
        window.bgMusic.play().catch(() => {{}});
    }}
    const lastTrigger = window.localStorage.getItem("rps_trigger");
    if (String(data.trigger) !== lastTrigger && data.event) {{
        window.localStorage.setItem("rps_trigger", data.trigger);
        if (data.event === "win") playSound(data.sounds.win);
        else if (data.event === "lose") playSound(data.sounds.lose);
        else playSound(data.sounds.click);
    }}
    </script>
    """
    components.html(html_code, height=0)

# ---------------------------------
# 4. Logic xử lý game
# ---------------------------------
choices = ["rock", "paper", "scissors"]

def get_result(player_choice, computer_choice):
    # TODO: Thử thách 3 - Quyết định Thắng, Thua, Hòa
    return "It's a tie!"

def play(player_choice):
    st.session_state.player_choice = player_choice
    st.session_state.computer_choice = random.choice(choices)
    
    # Lấy kết quả
    result = get_result(st.session_state.player_choice, st.session_state.computer_choice)
    st.session_state.result_text = result

    # TODO: Thử thách 4 - Cập nhật điểm và Kích hoạt âm thanh
   
    # else:
    #     st.session_state.last_event = "click"
    
    st.session_state.sound_trigger += 1

# ---------------------------------
# 5. Giao diện người dùng (UI)
# ---------------------------------
st.title("🐢 Game Oẳn Tù Tì (Practice)")

st.session_state.player_name = st.text_input("Nhập tên của em:", value=st.session_state.player_name)

# Khởi động âm thanh
render_audio()

# Hiển thị điểm
col_a, col_b = st.columns(2)
col_a.metric(st.session_state.player_name, st.session_state.player_score)
col_b.metric("Máy tính 🤖", st.session_state.computer_score)

st.divider()

if st.session_state.player_choice:
    disp1, disp2 = st.columns(2)
    with disp1:
        st.image(get_asset_path(IMAGE_PATHS[st.session_state.player_choice]), width=150)
    with disp2:
        st.image(get_asset_path(IMAGE_PATHS[st.session_state.computer_choice]), width=150)

st.divider()

st.subheader("Bấm nút để chơi:")
c1, c2, c3 = st.columns(3)

if c1.button("🪨 Búa (Rock)", use_container_width=True): play("rock")
if c2.button("📄 Bao (Paper)", use_container_width=True): play("paper")
if c3.button("✂️ Kéo (Scissors)", use_container_width=True): play("scissors")

st.divider()
st.markdown(f"<h2 style='text-align: center;'>{st.session_state.result_text}</h2>", unsafe_allow_html=True)

if st.button("Reset Game"):
    st.session_state.player_score = 0
    st.session_state.computer_score = 0
    st.session_state.result_text = "Hãy chọn một quân bài!"
    st.session_state.player_choice = None
    st.session_state.computer_choice = None
    st.rerun()
