let allPosts = [];

async function loadPosts() {
    const grid = document.getElementById('posts-grid');
    try {
        const response = await fetch('data/posts.json');
        allPosts = await response.json();
        
        renderPosts(allPosts);
        setupSearch();
        handleInitialHash(); // Manejar el link directo al cargar
    } catch (error) {
        console.error('Error loading posts:', error);
        grid.innerHTML = '<div class="card"><div class="card-content"><h3>Aún no hay artículos publicados.</h3><p>¡Vuelve pronto para ver las últimas tendencias!</p></div></div>';
    }
}

function renderPosts(posts) {
    const grid = document.getElementById('posts-grid');
    grid.innerHTML = '';
    
    // Mostramos los posts directamente (ya vienen invertidos o los manejamos aquí)
    posts.forEach((post, index) => {
        const card = document.createElement('div');
        card.className = 'card';
        card.onclick = () => openModal(post);
        card.innerHTML = `
            <div class="card-img-container">
                <img src="${post.image}" alt="${post.title}" class="card-img" onerror="this.src='https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=800'">
                <div class="card-overlay">
                    <span>SEGUIR LEYENDO</span>
                </div>
            </div>
            <div class="card-content">
                <div class="card-meta">
                    <span class="card-tag">${post.tag || 'Viral'}</span>
                    <span class="card-date">${post.date.split(' ')[0]}</span>
                </div>
                <h3>${post.title}</h3>
                <p>${extractExcerpt(post.content)}</p>
                <div class="read-more-btn">Leer noticia completa</div>
            </div>
        `;
        grid.appendChild(card);
    });
}

function extractExcerpt(html) {
    const tmp = document.createElement('DIV');
    tmp.innerHTML = html;
    const text = tmp.textContent || tmp.innerText || "";
    return text.substring(0, 120).trim() + "...";
}

function setupSearch() {
    const searchInput = document.createElement('input');
    searchInput.type = 'text';
    searchInput.placeholder = 'Buscar tendencias...';
    searchInput.className = 'search-bar';
    searchInput.oninput = (e) => {
        const term = e.target.value.toLowerCase();
        const filtered = allPosts.filter(p => 
            p.title.toLowerCase().includes(term) || 
            p.content.toLowerCase().includes(term)
        );
        renderPosts(filtered);
    };
    
    const container = document.querySelector('.hero');
    if (!document.querySelector('.search-bar')) {
        container.appendChild(searchInput);
    }
}

function openModal(post) {
    // Cambiar la URL sin recargar para que sea compartible
    const slug = createSlug(post.title);
    window.location.hash = slug;

    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.onclick = (e) => { if(e.target === modal) closeModal(); };
    
    modal.innerHTML = `
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal()">&times;</button>
            <div class="modal-header-img">
                <img src="${post.image}" alt="${post.title}" class="modal-img" onerror="this.style.display='none'">
                <div class="modal-img-gradient"></div>
            </div>
            <div class="modal-body">
                <div class="card-meta">
                    <span class="card-tag">${post.tag || 'Viral'}</span>
                    <span class="card-date">${post.date}</span>
                </div>
                <h1>${post.title}</h1>
                <div class="modal-text">${post.content}</div>
                
                <div class="modal-share">
                    <p>¡Comparte esta tendencia antes de que desaparezca!</p>
                    <div class="share-buttons">
                        <button class="btn-twitter" onclick="window.open('https://twitter.com/intent/tweet?text=${encodeURIComponent(post.title)}&url=${encodeURIComponent(window.location.href)}')">Twitter</button>
                        <button class="btn-telegram" onclick="window.open('https://t.me/share/url?url=${encodeURIComponent(window.location.href)}&text=${encodeURIComponent(post.title)}')">Telegram</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
    document.body.style.overflow = 'hidden';
}

function createSlug(text) {
    return text.toString().toLowerCase().trim()
        .replace(/\s+/g, '-')
        .replace(/[^\w\-]+/g, '')
        .replace(/\-\-+/g, '-');
}

function handleInitialHash() {
    const hash = window.location.hash.replace('#', '');
    if (hash) {
        const post = allPosts.find(p => createSlug(p.title) === hash);
        if (post) openModal(post);
    }
}

function closeModal() {
    const modal = document.querySelector('.modal-overlay');
    if (modal) {
        modal.remove();
        document.body.style.overflow = 'auto';
        history.pushState("", document.title, window.location.pathname + window.location.search);
    }
}

document.addEventListener('DOMContentLoaded', loadPosts);
