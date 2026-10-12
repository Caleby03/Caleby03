<div align="center">

# Hi, I'm Caleb 👋  
### Full-Stack Developer | Founder @ Arcanet Consulting | Product-Focused Builder

<img src="https://readme-typing-svg.demolab.com?font=Inter&weight=600&size=24&duration=2600&pause=850&color=3B82F6&center=true&vCenter=true&width=900&lines=Building+clean%2C+scalable+web+applications;Exploring+autonomous+browser+agents;Turning+ideas+into+real+software" alt="Typing SVG" />

<br/>

[![GitHub](https://img.shields.io/badge/GitHub-Caleby03-181717?style=for-the-badge&logo=github)](https://github.com/Caleby03)
[![Arcanet](https://img.shields.io/badge/Website-arcanettechnology.com-2563EB?style=for-the-badge&logo=googlechrome&logoColor=white)](https://arcanettechnology.com)

</div>

---

## 🚀 About Me

- 💻 I build software across **frontend, backend, and systems-level projects**
- 🏢 Founder of **[Arcanet Consulting](https://arcanettechnology.com)** — hands-on engineering help for startups and small teams, from architecture to shipping
- 🤖 I’m especially interested in **autonomous/intelligent browser workflows**
- 🎯 Current focus: **shipping impactful projects and improving software craftsmanship**

---

## 🧰 Tech Stack

<div align="center">

### Languages
<img src="https://skillicons.dev/icons?i=python,ts,js,html,css,php,c" />

### Frameworks & Runtime
<img src="https://skillicons.dev/icons?i=react,nextjs,nodejs,express,fastapi,tailwind" />

### Cloud, Deployment & Data
<img src="https://skillicons.dev/icons?i=cloudflare,vercel,aws,gcp,supabase,mysql,mongodb" />

### Tools
<img src="https://skillicons.dev/icons?i=git,github,vscode,linux,docker" />

</div>

---

## 🌟 Featured Projects

### 🖧 Three-Node Homelab — Infrastructure as Config
**Live:** [caleby03.github.io/Homelab-Portfolio](https://caleby03.github.io/Homelab-Portfolio/) · **Repo:** [Caleby03/Homelab-Portfolio](https://github.com/Caleby03/Homelab-Portfolio)

<a href="https://caleby03.github.io/Homelab-Portfolio/">
  <img src="assets/screenshots/homelab.jpg" width="640" alt="Homelab portfolio — architecture, operational practice and build status rendered as a monitoring dashboard" />
</a>

A self-hosted homelab run as infrastructure-as-config, built around a deliberate split of responsibilities: an always-on mini PC for stateful services, a Windows workstation used as burst GPU capacity, and a Raspberry Pi as an independent watchdog. Every node is assigned work it is actually suited to, every container is capacity-bounded, and the monitoring is designed around the assumption that any node — including the one doing the monitoring — will eventually fail.

- **Containerized service stacks** split by *lifecycle and failure domain* rather than by subject matter, so alerting can't be taken down by the same command that takes down the thing it watches
- **GitOps deployment** — stacks deploy straight from a git repo and reconcile on their own, so a commit is the deploy
- **Zero-trust networking** over a WireGuard mesh: no port forwarding, no public ingress, access authenticated per device rather than per network
- **Found and closed a live security gap** — an audit revealed published container ports reachable from the LAN, because Docker inserts its own iptables rules ahead of the chain the host firewall manages, so a `deny incoming` policy silently did not apply. Moved enforcement into the `DOCKER-USER` chain and verified it across reboot, daemon restart, and from an off-network host
- **Metrics and dashboards** with recording rules pre-computing dashboard values, plus **Architecture Decision Records** written at the time each choice was made rather than reconstructed afterward

**Stack:** Docker · Docker Compose · Portainer · Prometheus · Grafana · Tailscale · iptables/UFW · PostgreSQL · Redis · Ubuntu

---

### 🏢 Arcanet Consulting
**Site:** [arcanettechnology.com](https://arcanettechnology.com)

<a href="https://arcanettechnology.com">
  <img src="assets/screenshots/arcanet.jpg" width="640" alt="Arcanet Consulting homepage — hands-on software engineering & technology consulting" />
</a>

My software engineering & technology consulting practice. I work directly with founders and small teams — hands-on, no hand-offs — to design, build, and modernize software, from architecture and cloud setup through shipping the actual product. The pitch is how I work: direct, honest scoping, and shipping without cutting the corners that come back later.

- **Custom software** — web apps, APIs, and internal tools built to be maintainable
- **Cloud & infrastructure** — architecture, migrations, and CI/CD on AWS, GCP, Azure, and Cloudflare
- **Technical strategy** — system design, code and architecture reviews, and honest build-vs-buy advice
- **Product delivery** — scoping, prioritizing, and shipping from MVP to launch

**Engagements:** project-based or ongoing · work directly with the person doing the work

---

### 🏠 Harmony House NC
**Repo:** `Caleby03/HarmonyHouseWebapp` *(private)*

<img src="assets/screenshots/harmony-house.jpg" width="640" alt="Harmony House NC landing page — a mountain retreat booking site with a live availability search" />

A direct-booking and calendar-sync platform for **Harmony House NC**, a short-term rental in the Blue Ridge Mountains of North Carolina catering to wedding parties and equestrian guests. Guests book directly on the property's own site instead of paying platform fees on Airbnb or Vrbo.

- **Live availability calendar** with direct date selection and instant booking
- **Square** Web Payments for checkout; **Resend** for confirmation and cancellation emails
- **Automatic calendar sync** — a **GitHub Actions** cron ingests Airbnb & Vrbo iCal feeds every 15 minutes so availability is always accurate
- **Host portal** (`/portal`): reservation list, platform-color-coded calendar, revenue & occupancy metrics, property editor, and date blocking

**Stack:** Next.js 16 · React 19 · Tailwind v4 · FastAPI · SQLModel · PostgreSQL · Square · Resend · Railway

---

### 🤖 Intelligent Browser Agents
**Repo:** [Caleby03/Intelligent-Browser-Agents](https://github.com/Caleby03/Intelligent-Browser-Agents) · UCF Senior Design (Team L07)

<img src="assets/screenshots/intelligent-browser-agents.png" width="640" alt="Intelligent Browser Agents — Live Agent View streaming a browser session in real time while the agent reasons through a task" />

A platform that turns natural-language instructions into real actions performed on a live browser session. Users delegate repetitive digital chores — filling forms, navigating dashboards, downloading files — to an agent that reads the page, plans, and executes visually and safely, with the whole run streamed back to the UI in real time.

- **LLM-driven agent runtime** built on **LangGraph** — an orchestrator → executor → verifier → fallback/interaction loop
- **Playwright** browser automation with ARIA-oriented DOM extraction and a modular action layer (navigate, click, type, search, scroll, press_key, wait, extract_content)
- **Human-in-the-loop (HITL):** the agent pauses to ask for clarifications, approvals, or credentials mid-run
- Live browser frames, logs, and agent reasoning streamed to the frontend over **WebSockets**
- Full account system + encrypted storage of reusable credentials and profile data for automation contexts

**Stack:** React + Vite · FastAPI · LangGraph · Playwright · PostgreSQL · WebSockets · AWS (LightSail/EC2)

**Demo Video:** [Watch on YouTube](https://youtu.be/CmKoODnEdDQ?si=L1nCML-f8zLrPcDL) · **Showcase:** [UCF Senior Design page](https://www.cecs.ucf.edu/SeniorDesignShowcase/team/intelligent-browser-agents/)

---

## 📊 GitHub Analytics

<div align="center">

<img src="assets/metrics/overview.svg" alt="GitHub stats: contributions, repositories, stars and followers" />
<br/>
<img src="assets/metrics/languages.svg" alt="Most-used languages across public repositories" />
<br/>
<img src="assets/metrics/streak.svg" alt="Contribution calendar with current and longest streak" />

<sub>Generated twice daily by a GitHub Action · contribution counts include private work; languages reflect public repos</sub>

</div>

---

## 🔎 Live Profile Details

<div align="center">
  <img src="https://komarev.com/ghpvc/?username=Caleby03&style=for-the-badge&color=2563EB" alt="profile views" />
</div>
