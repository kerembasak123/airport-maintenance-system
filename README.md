<p align="center">
  <h1 align="center">✈️ Airport Terminal Electronic Systems & Maintenance Management Automation</h1>
  <p align="center">
    An enterprise-grade Django web platform designed to automate technical operations, equipment lifecycle tracking, periodic maintenance scheduling, and role-based feedback workflows across airport terminal facilities.
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django" />
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5" />
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</p>

---

## 📌 About The Project

Airport technical infrastructures require rigorous tracking, scheduled maintenance, and real-time operational feedback. **Airport Terminal Electronic Systems & Maintenance Management Automation** is a comprehensive Web System engineered to streamline ground operations, automate routine equipment servicing, and eliminate manual log errors.

From high-level terminal and block mapping down to individual device serial number inspection via **QR Code Scanning**, the platform offers end-to-end management for airport electronics engineers and field technicians.

---

## ✨ Key Technical Modules & Features

### 🏢 1. Facility & Device Infrastructure Mapping
* **Terminal & Block Mapping:** Organize airport hardware hierarchically based on Terminal structures, specific Blocks, and operational Zones.
* **Serial Number Tracking:** Unique identification for every electronic asset registered in the airport inventory.
* **QR Code Integration:** Fast scan-and-read QR system for quick hardware identification, status lookup, and field inspection.

### 👥 2. Role-Based Portal Architecture (RBAC)
* **Engineer Portal:** 
  * Full administrative control over system assets and task distribution.
  * Assigns maintenance schedules, oversees fault tickets, and reviews field reports.
  * High-level reporting dashboards for system availability and maintenance history.
* **Technician Portal:**
  * View assigned daily maintenance schedules and hardware work orders.
  * Perform field inspections, fill interactive maintenance forms, and update device operational statuses.

### 🛠️ 3. Maintenance Cycles & Periodic Task Scheduling
* **Periodic Maintenance Engine:** Configure dynamic maintenance intervals (daily, weekly, monthly, quarterly) per equipment type.
* **Maintenance History Logs:** Comprehensive historical ledger detailing past failures, replaced components, and technician logs.
* **Interactive Maintenance Forms:** Standardized web forms (`bakim_form`) ensuring structured data input for all inspections.

### 📧 4. Task Feedback & Email Notification System
* **Real-time Task Feedback:** Technicians can submit instant work updates, fault notices, or completion confirmations (`gorev_geri_bildirimi`).
* **Automated Email Notifications:** Triggers instant automated email alerts to supervising engineers upon task updates, critical equipment failures, or schedule overdues.

---

## 💻 Tech Stack & Architecture

* **Backend:** Python / Django Framework
* **Frontend:** HTML5, Custom Responsive CSS Modules (`style.css`, `cihaz_listesi.css`, `raporlar.css`, etc.), JavaScript
* **Database:** Relational SQLite (Development) / PostgreSQL-ready
* **Notification Engine:** SMTP Email Service Integration
* **Asset Tracking:** QR Code Encoder / Decoder Interface

---

## 📁 UI & CSS Architecture Overview

The system UI features dynamic, dedicated modular stylesheets for enhanced user experience and clear separation of operational views:
* `giris.css` / `kayit.css`: Authentication & Role-based authorization entryways.
* `cihaz_listesi.css` / `cihaz_duzenle.css`: Asset inventory grids and management interfaces.
* `bakim_form.css` / `cihaz_bakim_gecmisi.css`: Field inspection logs and archival reports.
* `gorevler.css` / `gorev_form.css` / `gorev_geri_bildirimi.css`: Task assignment and feedback feedback pipelines.
* `raporlar.css`: Executive reporting analytics for engineers.

---

## 🚀 Getting Started

Follow these steps to set up the project locally:

### Prerequisites

* Python 3.8+ installed
* Pip package manager

### Installation & Local Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/kerembasak123/terminal_elektronik_sistemleri_bakim_otomasyonu.git](https://github.com/kerembasak123/terminal_elektronik_sistemleri_bakim_otomasyonu.git)
   cd terminal_elektronik_sistemleri_bakim_otomasyonu
