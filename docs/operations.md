# Installation and operations

## Prepared hosts

| Host | Application | Inference | Database |
| --- | --- | --- | --- |
| Mac mini, primary Docker deployment | `~/Services/flagcity-navigator`, project `flagcity-navigator`, `127.0.0.1:8878` | Dedicated Apple Silicon runtime, `127.0.0.1:8879` | Compose volume `flagcity-navigator_navigator_state` |
| MacBook, offline demo | Local `Flagstaff-Navigator` folder, same loopback port | Dedicated Apple Silicon runtime and weights | Project-local `.state/navigator.sqlite3` |

## Reproduce the Mac mini Docker deployment

Use Bash or Zsh with Docker Desktop running. Transfer this source folder to the Mac mini’s new service directory. The pinned Qwen model and llama.cpp macOS runtime download once. Setup requires about 1.2 GB for the model, plus room for Docker’s Python image. The app uses only the Python standard library.

```sh
cd ~/Services/flagcity-navigator
./scripts/install-model.sh
mkdir -p .state
nohup ./scripts/start-model.sh > .state/model.log 2>&1 </dev/null &
echo $! > .state/model.pid
docker compose up -d --build --wait
curl -fsS http://127.0.0.1:8878/api/health
python3 scripts/rehearse.py --require-model
```

Expected health is `"status": "ok", "model_ready": true` after weights load. The app starts while the model loads. The model process is separate from Docker and should be started again after a Mac mini reboot or login restart. The Compose app restarts itself while Docker Desktop is running.

To view the Mac mini from a laptop, forward to a free local port. This keeps the MacBook demo port available.

```sh
ssh -N -L 18878:127.0.0.1:8878 macmini
```

Open `http://127.0.0.1:18878`. Mac mini port 8878 stays bound to loopback. Rule-only deployment is available with `NAV_MODEL_URL='' docker compose up -d --build --wait`.

## Public demo route

[flagproject.chrisclark.tech](https://flagproject.chrisclark.tech) uses the existing **MacMini Docker** connector. Its dedicated Published Application route forwards only this hostname to `http://host.docker.internal:8878`. The original Flagstaff hostname uses its own route. No new connector credentials or public host port are required.

The Mac mini project has a local `.env` with `NAV_PUBLIC_HOST=flagproject.chrisclark.tech`. Compose passes this setting to the app so it accepts the hostname and the matching HTTPS request origin. After a deployment, check the public health endpoint and complete a fictional interview to verify both reads and writes. Use the Cloudflare dashboard to remove this specific route when the public demo ends. [Cloudflare published application routes](https://developers.cloudflare.com/tunnel/)

## Present without Wi-Fi

On the presenting MacBook, run `./scripts/install-model.sh` once while online if assets have yet to be prepared. Apple Silicon macOS with Python 3.9+ is required for the included launcher. Start the app and model independently of the Mac mini:

```sh
./scripts/demo-up.sh
```

Open `http://127.0.0.1:8878` and reload once the footer says **Local AI ready**. Disconnect Wi-Fi and rehearse one complete interview in the regular browser. Keep the local deck, script and exported assessments open in separate windows. If model startup is slow or unavailable, **Local rules ready** can conduct the interview and generate the assessment. If the app fails, use the preserved export as evidence from a previously executed session.

For a separate rules-only rehearsal, use `NAV_MODEL_URL='' NAV_PORT=8880 NAV_DB=.state/rules-only.sqlite3 ./scripts/start-local.sh`, then open `http://127.0.0.1:8880`. The install script verifies hashes for the [Qwen model](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF) and [llama.cpp release](https://github.com/ggml-org/llama.cpp/releases/tag/b12359).

## Analyst access

The management dashboard is at `/analyst`. Its reports, filters and downloads require the demo analyst sign-in. The username is `analyst`. On a fresh installation, set a unique password of at least 16 characters. The command prompts without echoing the password. Changing it signs out prior analyst sessions.

```sh
# Docker on the Mac mini
docker compose exec navigator python server.py --set-analyst-password

# Native MacBook copy
python3 server.py --set-analyst-password
```

Use HTTPS for the public dashboard. It shows the Mac mini database. The MacBook runs independently and shows only assessments saved to its local database. The dashboard counts completed records only. Older submissions without a benefit rating appear as **Not estimated**. Use **Find assessment** and the participant’s 12-character ID to open the record. The follow-up contact is visible in the signed-in detail view when available. **Mark reviewed** records human review, and **Draft follow-up email** opens a draft in the analyst’s mail app for manual sending. Older submissions can have no saved contact. The shared demo analyst account uses a salted password hash and expiring sessions. A City pilot would need individual sign-in, role-based access and review of audit and retention requirements.

**Change review status** records where work stands. **Awaiting review** is the intake queue, **Reviewed** records initial triage, **Needs information** pauses for a follow-up, **Approved for next step** records the go-ahead to proceed with the reviewed handoff, and **Closed** ends the request. If the original assessment flagged a hold, **Mark reviewed** changes the badge to **Governance review required**. Approval requires the analyst to confirm clearance from the required reviewers and save a reference or note. Closing a flagged case removes it from active hold counts and keeps the flags in its record. Participant receipts show the status, and signed-in analysts can read the note. Earlier review timestamps and the original assessment export are preserved.

**Request at a glance** works on existing assessments. The app saves the local AI summary on first successful generation. If the model is stopped, saved summaries remain available and other assessments show an excerpt from the confirmed intake. The app stores the summary alongside the intake in SQLite under the same analyst access. Downloads use the saved assessment and interview evidence. For earlier reports, the app renders the current governance-first layout from those saved records.

## Support and recovery

- See `docker compose ps` and `docker compose logs --tail=40 navigator`. Check model health on port 8879 if the application health shows model unavailable. There are no transcript or token values in normal request logs.
- `docker compose stop navigator` stops the new service while preserving its database. Restart using `docker compose up -d --wait`. Use the image and source matching the intended rule version when rolling back.
- Back up using SQLite’s online backup API or stop the service before copying the database and its WAL sidecars from the dedicated volume. Test restoration in a separate volume and compare report IDs and exports before replacing any working service. If a pilot needs stronger recovery guarantees, agree on backup frequency, restore time and post-restore reconciliation with the process owner.
- Demo records persist in the selected development database. The demo has one analyst account. Automated retention, institutional sign-in and a production audit pipeline are pilot requirements. Use invented workflow and contact details during the exercise. Contact fields live in a separate, readable SQLite table and stay out of model requests and exports. Decide the authorized pilot retention, purge and access policy before accepting any real workflow information.
