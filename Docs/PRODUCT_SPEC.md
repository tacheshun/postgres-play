#  MVP product spec: “PulseScope”

A privacy-first contextual stress & recovery app for Apple Watch with real-time micro-coaching and next-day recovery scoring.

## 1) Users and constraints
	•	Target: busy humans with a pulse, not hospital patients. Wellness, not diagnosis.
	•	Hardware: Apple Watch Series 8 or newer recommended for wrist temperature; runs on SE/Series 6+ with reduced features.  ￼
	•	OS: watchOS 11/26 and iOS 18/18.1+ (map to your current device support). New OS adds background/task tweaks and first-party fitness features you don’t rely on.  ￼
	•	Privacy: on-device by default. Cloud export optional and off.

## 2) Core value
	•	Today card: Recovery score each morning, with concrete “do this, not that.”
	•	Live stress nudge: Detect acute stress spikes during the day and trigger a 60–90s breathing drill or quick walk prompt.
	•	Weekly trend: What actually moved your stress/recovery last 7 days, with simple habits to try.

No medical promises. No “you have a disease.” Just useful signals and coaching.

## 3) Signals & data (v1)
	•	Overnight (for recovery):
	•	HRV (SDNN), resting HR, respiratory rate, sleep stages/efficiency, sleeping wrist temperature delta. HealthKit exposes these; wrist temp is sleep-only and Series 8+.  ￼
	•	Daytime (for stress spikes):
	•	Heart rate, interbeat interval variance surrogate from PPG windows, accelerometer/gyroscope features, calendar activity context (optional), environmental noise (optional).
	•	Workout mode when needed for higher-rate HR and longer runtime. HKWorkoutSession boosts HR sample frequency and sensor fidelity.  ￼

## 4) Feature set (MVP scope)

A. Recovery (daily, phone-side heavy)
	•	28-day rolling baseline of HRV, resting HR, wrist temp, respiratory rate, sleep efficiency.
	•	Compute z-scores per metric; fuse via weighted sum with guardrails.
	•	Output Recovery 0–100 plus two drivers: “HRV −0.7σ, Temp +0.5σ.”
	•	Action card: 1–2 things to do today based on drivers (shorter workout, earlier bedtime, hydration).

B. Acute stress (watch-side, real-time)
	•	30–60 second windows: median HR, short-window HRV surrogate, motion jitter, posture change.
	•	Micro-classifier with hysteresis to avoid flip-flopping; gate on skin contact/motion quality.
	•	If confidence > threshold and user is not in a workout, show Nudge: start 1-minute breathing or 3-minute walk timer.

C. Complications & UI
	•	Watch complication: “Recovery 72 | Stress low.”
	•	Watch App: “Now” tab with stress gauge and quick actions; “Today” tab with drivers; “Log” tab for 7-day micro-timeline.
	•	iPhone App: recovery trend, factor breakdown, and export PDF summary.

D. Background behavior
	•	Background delivery for HealthKit changes.
	•	WKExtendedRuntimeSession during optional “Focus Session” or under a Workout umbrella for higher-rate sensing when the user opts in. Expect throttling outside active sessions.  ￼

## 5) ML plan

On-watch (real-time)
	•	Model: tiny gradient-boosted tree or 1D CNN on 8–12 features per 5s hop. Quantized Core ML.
	•	Why on-watch: lower latency, immediate UX, no radio needed. Core ML supports watchOS inference.  ￼
	•	Fail-safes: pause when motion artifact is high; don’t alert during high-intensity workouts.

On-phone (nightly)
	•	Model: temporal fusion of multi-day features for recovery scoring; simple Bayesian smoothing for baselines.
	•	Personalization: weekly recalibration of thresholds from EMA labels and adherence logs.

## 6) Data model (HealthKit + app store)
	•	HealthKit read permissions: Heart Rate, HRV (SDNN), Resting HR, Respiratory Rate, Sleep Analysis, Apple Sleeping Wrist Temperature, Workouts, Environmental Audio Exposure (optional).  ￼
	•	App container:
	•	DailyMetrics { date, hrv_z, rhr_z, temp_z, rr_z, sleep_eff_z, recovery_score, drivers[] }
	•	StressEvents { ts, conf, features[], user_action }
	•	Labels { ts, self_reported_stress: 1–5 }
	•	Settings { quiet_hours, alert_threshold, data_retention_days }

## 7) Tech stack
	•	watchOS: Swift, SwiftUI, HealthKit, CoreMotion, Core ML, WatchConnectivity.
	•	iOS: SwiftUI, HealthKit, BackgroundTasks, Core ML, PDFKit for export.
	•	No Flutter UI on watch; if you insist on Flutter for iOS, you still build a separate native watch target and bridge with WatchConnectivity. This is fragile and not worth it for v1.  ￼
	•	Kotlin Multiplatform is viable only for sharing algorithms as a framework; watch UI remains SwiftUI. It works, but adds complexity you don’t need for an MVP.  ￼

## 8) False-positive control
	•	Two-signal rule: only alert if at least two independent signals deviate (e.g., HR up + IBI variance down) and motion artifact is low.
	•	Hysteresis + cooldown: minimum 10 minutes between alerts; decay filter on the score.
	•	Context gating: no alerts during workouts, meetings flagged as “presenting,” or quiet hours.

## 9) Edge cases
	•	Tattoos, loose band, cold skin → quality flag and “tighten band” hint.
	•	SpO₂ is a regional/legal mess; treat as optional, never core logic.
	•	Background refresh isn’t guaranteed; design around workout/extended sessions for any sustained sensing.  ￼

## 10) Monetization toggles (future)
	•	Free: daily recovery + basic nudges.
	•	Pro: advanced trends, CSV/PDF export, custom schedules, Apple Health auto-exports.


#  Repo layout
```
PulseScope/
  Packages/
    PulseCore/               # shared logic, math, feature extraction
    PulseML/                 # model wrapper, feature scaling, versioning
  iOS/
    PulseScopeApp/
      Views/, ViewModels/, Services/
      HealthKit/, Export/
  watchOS/
    PulseScopeWatch/
      Complications/, Sessions/   # HKWorkoutSession, WKExtendedRuntimeSession
      RealtimeInference/
      UI/
  Tools/
    ModelTraining/           # notebooks/scripts (Python/Swift) to train tiny model
  Docs/
    PRODUCT_SPEC.md
    PRIVACY.md
```