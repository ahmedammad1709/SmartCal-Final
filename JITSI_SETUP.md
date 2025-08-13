# Jitsi Integration for SmartCal

This document provides instructions for setting up and using the Jitsi video conferencing integration with SmartCal.

## 1. Jitsi Server Options

### Option 1: Use the Public Jitsi Server (Recommended)

The application is configured to use the public Jitsi server at https://meet.jit.si by default. This requires no additional setup and works immediately.

### Option 2: Local Setup (Jitsi Installation via Docker)

If you prefer to run your own Jitsi server:

1. Install Docker and Docker Compose on your local PC.

2. In the terminal, run:

```bash
git clone https://github.com/jitsi/docker-jitsi-meet && cd docker-jitsi-meet
cp env.example .env
./gen-passwords.sh
docker-compose up -d
```

3. After setup, Jitsi will be available locally at: https://localhost:8443

4. Accept the browser's self-signed certificate warning when testing locally.

5. Update the `app.py` file to use your local Jitsi server by modifying the `jitsi_link` generation code.

## 2. Database Migration

Run the database migration script to add the necessary columns to the bookings table:

```bash
python update_db_schema.py
```

## 3. How It Works

### Jitsi Link Generation

When a booking is confirmed in the backend:

1. A unique room name is generated using the booking details: `smartcal-{agenda_id}-{timestamp}`
2. The room name and full meeting link are stored in the database along with the booking.
3. The meeting link is constructed using the public Jitsi server: `https://meet.jit.si/{room_name}`
4. This ensures the link works for both host and visitor without requiring any local setup.

### Email Notifications

Both the host and guest receive email notifications containing:

- Meeting details (date, time, duration)
- The Jitsi meeting link to join the video conference

### Dashboard Integration

In the "Upcoming Meetings" tab of the SmartCal dashboard, each booked meeting now includes a "Start Meeting" button that redirects to the Jitsi meeting room URL.

## 4. Usage Flow

1. Guest books a meeting via the public booking page.
2. Backend generates a Jitsi room name and link, stores it, and sends it in confirmation emails to both parties.
3. The "Upcoming Meetings" tab in the dashboard shows a "Start Meeting" button for each booking.
4. At the scheduled time, both host and guest click the link to join the Jitsi room.

## 5. Production Deployment

For production deployment, you can either:

1. Continue using the public Jitsi instance at `meet.jit.si` (recommended for simplicity).
2. Set up your own Jitsi server using the Docker setup above and configure it with proper SSL certificates.

If you want to use your own Jitsi server, you'll need to modify the `app.py` file to use your custom Jitsi URL instead of the public one.