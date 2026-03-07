# Gulf Watch v4 - Collaboration Branch

**Status:** Experimental / In Development  
**Base:** Gulf Watch v2 (stable)  
**Purpose:** Collaborative development space for new features

---

## 🎯 What is this?

This is the **v4-collab** branch of Gulf Watch - a sandbox for experimenting with new features, designs, and improvements while keeping v2 (main branch) stable and operational.

**v2 (main)** = Stable, production, no experiments  
**v4-collab** = Experimental, collaborative, new features

---

## 🤝 How to Collaborate

### For Collaborators:

1. **Fork this repository** to your GitHub account
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/gulf-watch-v2.git
   cd gulf-watch-v2
   ```
3. **Switch to v4-collab branch**:
   ```bash
   git checkout v4-collab
   ```
4. **Create your feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
5. **Make changes, commit, push to your fork**
6. **Submit Pull Request** to `nKOxxx/gulf-watch-v2` targeting `v4-collab` branch

### Branch Strategy:

```
main (v2) ──────── stable, production
    │
    └── v4-collab ─── experimental, collaborative
         │
         ├── feature/mobile-redesign
         ├── feature/ai-summaries
         ├── feature/user-auth
         └── your-feature-here
```

---

## 🚀 Current Experiments

| Feature | Status | Lead | Description |
|---------|--------|------|-------------|
| Mobile-first redesign | Planning | TBD | Better mobile UX |
| AI-powered summaries | Planning | TBD | Auto-summarize news |
| User accounts | Planning | TBD | Save favorites, alerts |
| Push notifications | Planning | TBD | Mobile/web push |
| Your idea here | - | You | - |

---

## 🛠️ Development Setup

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build
```

---

## 📋 Guidelines

### DO:
- ✅ Experiment freely
- ✅ Break things (it's expected)
- ✅ Propose wild ideas
- ✅ Learn and iterate
- ✅ Document what you try

### DON'T:
- ❌ Merge to `main` without approval
- ❌ Delete or modify v2 stable code without backup
- ❌ Push API keys or secrets
- ❌ Worry about breaking v4 (that's what it's for)

---

## 🎨 Design Principles for v4

1. **Mobile-first** - Most users are on phones
2. **Fast** - Sub-3 second load times
3. **Reliable** - Work offline, handle errors gracefully
4. **Clear** - Users instantly understand what they're seeing
5. **Useful** - Every feature solves a real problem

---

## 💡 Feature Ideas

Want to work on something? Pick from below or propose your own:

### High Priority
- [ ] Complete mobile redesign
- [ ] Better news filtering (by severity, source type)
- [ ] Push notifications for critical alerts
- [ ] User accounts (save favorites)

### Medium Priority
- [ ] AI-generated news summaries
- [ ] Historical incident archive
- [ ] Better map interactions
- [ ] Dark/light theme toggle

### Experimental
- [ ] Telegram bot integration
- [ ] WhatsApp alerts
- [ ] Multi-language support (Arabic)
- [ ] Audio briefings (text-to-speech)

---

## 🔄 Deployment

**v4-collab** auto-deploys to: `https://gulf-watch-v4.vercel.app` (when set up)

**v2 (main)** stays at: `https://gulf-watch-v2.vercel.app` (never touched)

---

## 📞 Questions?

- Open an issue on GitHub
- Tag @nKOxxx in PRs
- Discuss in PR comments

---

**Let's build something great together!** 🚀
