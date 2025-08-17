// static/script.js - minimal AJAX front-end
const boardEl = document.getElementById('board');
const messageEl = document.getElementById('message');
const scoreEl = document.getElementById('score');
const difficultyEl = document.getElementById('difficulty');
const playerSymEl = document.getElementById('player_sym');
const newBtn = document.getElementById('newBtn');
const replayBtn = document.getElementById('replay');
const resetScoresBtn = document.getElementById('resetScores');
// Add this near the top of script.js
const voiceToggle = document.getElementById('voiceToggle');
let femaleVoice = null;

// Load voices once they are available
window.speechSynthesis.onvoiceschanged = () => {
    const voices = window.speechSynthesis.getVoices();
    femaleVoice = voices.find(voice => 
        voice.name.toLowerCase().includes('zira') ||
        voice.name.toLowerCase().includes('samantha') ||
        voice.name.toLowerCase().includes('female')
    );
};


// original
// function speak(msg){
//   if(voiceToggle.checked && 'speechSynthesis' in window){
//     const utter = new SpeechSynthesisUtterance(msg);
//     utter.lang = 'en-US';
//     window.speechSynthesis.speak(utter);
//   }
// }

// //updated
// function speak(msg){
//   if(voiceToggle.checked && 'speechSynthesis' in window){
//     const utter = new SpeechSynthesisUtterance(msg);
//     utter.lang = 'en-US';
    
//     // Pick a female voice if available
//     const voices = window.speechSynthesis.getVoices();
//     const femaleVoice = voices.find(voice => voice.name.toLowerCase().includes('female') || voice.name.toLowerCase().includes('zira') || voice.name.toLowerCase().includes('samantha'));
//     if(femaleVoice) utter.voice = femaleVoice;
    
//     window.speechSynthesis.speak(utter);
//   }
// }

// again updated and modified part
function speak(msg){
  if(voiceToggle.checked && 'speechSynthesis' in window){
    const utter = new SpeechSynthesisUtterance(msg);
    utter.lang = 'en-US';
    
    if(femaleVoice) utter.voice = femaleVoice; // use Zira if available
    utter.rate = 0.9; // slower than default (0.5 - 2.0 range)
    utter.pitch = 1;   // keep normal pitch
    window.speechSynthesis.speak(utter);
  }
}



function createCells() {
  boardEl.innerHTML = '';
  for(let i=0;i<9;i++){
    const d = document.createElement('div');
    d.className = 'cell';
    d.id = 'c'+i;
    d.dataset.idx = i;
    d.innerText = (i+1);
    d.addEventListener('click', onCellClick);
    boardEl.appendChild(d);
  }
}

async function api(path, method='GET', body=null){
  const opts = {method, headers:{'Content-Type':'application/json'}};
  if(body) opts.body = JSON.stringify(body);
  const res = await fetch(path, opts);
  return await res.json();
}

function updateUI(state){
  // board
  state.board.forEach((v,i)=>{
    const el = document.getElementById('c'+i);
    el.classList.remove('player','ai','win');
    if(v === ' '){
      el.innerText = (i+1);
    } else {
      el.innerText = v;
      if(v === state.player_sym) el.classList.add('player');
      else el.classList.add('ai');
    }
  });
  // highlight winning line
  if(state.winning_line){
    state.winning_line.forEach(i=>{
      document.getElementById('c'+i).classList.add('win');
    });
  }
  // message and score
  messageEl.innerText = state.message || '';
  speak(state.message || '');  // ADD THIS LINE
  scoreEl.innerText = `Wins ${state.scores.wins} | Losses ${state.scores.losses} | Ties ${state.scores.ties}`;
  difficultyEl.value = state.difficulty || 'medium';
  playerSymEl.value = state.player_sym || 'X';
}

async function fetchState(){
  // calling / to ensure session is there, then request /api/new as an initial state
  const res = await api('/api/new', 'POST', { difficulty: difficultyEl.value, player_sym: playerSymEl.value, player_starts: true });
  updateUI(res);
}

async function onCellClick(e){
  const idx = parseInt(this.dataset.idx);
  try{
    const res = await api('/api/move', 'POST', { index: idx });
    if(res.error){
      // ignore or show toast.
    } else updateUI(res);
  }catch(err){
    console.error(err);
  }
}

newBtn.addEventListener('click', async ()=>{
  const res = await api('/api/new', 'POST', { difficulty: difficultyEl.value, player_sym: playerSymEl.value, player_starts: true });
  updateUI(res);
  speak(res.message || 'New game started!');  // ADD THIS LINE
});

replayBtn.addEventListener('click', async ()=>{
  const res = await api('/api/new', 'POST', { difficulty: difficultyEl.value, player_sym: playerSymEl.value, player_starts: true });
  updateUI(res);
  speak(res.message || 'New game started!');  // ADD THIS LINE
});

resetScoresBtn.addEventListener('click', async ()=>{
  const res = await api('/api/reset_scores', 'POST');
  updateUI(res);
});

// init
createCells();
fetchState();
