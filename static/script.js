
// Dark mode toggle
function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
}

// Simple alert for new comment
function showAlert() {
    alert("Welcome to the blog! Enjoy reading and commenting 😊");
}
// ===== API-enhanced comments =====

// Load comments initially
async function loadComments() {
    const res = await fetch('/api/comments');
    const data = await res.json();
    updateComments(data);
}

// Update comment list dynamically
function updateComments(comments) {
    const list = document.querySelector('ul'); // Your existing <ul> for comments
    list.innerHTML = '';
    comments.forEach(c => {
        const li = document.createElement('li');
        li.innerHTML = `<strong>${c.name}</strong>: ${c.comment} <button onclick="alert('Liked!')">👍</button>`;
        list.appendChild(li);
    });
}

// Handle form submission
const form = document.querySelector('form'); // Your existing form
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = form.name.value;
    const comment = form.comment.value;

    const res = await fetch('/api/comments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, comment })
    });

    const data = await res.json();
    updateComments(data.comments);
    form.reset();
});

// Call initially
loadComments();
// Contact form submission
const contactForm = document.querySelector('.contact-form form');

contactForm.addEventListener('submit', async (e) => {
    e.preventDefault(); // prevent page reload

    const name = contactForm.querySelector('input[name="name"]').value;
    const email = contactForm.querySelector('input[name="email"]').value;
    const msg = contactForm.querySelector('textarea').value;

    // For now, just show an alert (no backend)
    alert(`Thank you ${name}! Your message has been sent.`);

    // Reset the form
    contactForm.reset();
});