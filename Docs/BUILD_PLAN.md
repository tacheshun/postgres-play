# Build plan

## Week 1: Project skeleton & Foundation
### Goals
- Complete Xcode workspace setup with proper architecture
- Establish foundational infrastructure for both iOS and watchOS apps

### Tasks
1. **Project Setup**
   - Create Xcode workspace with iOS app target (deployment target: iOS 18.0+)
   - Create independent watchOS app target (deployment target: watchOS 11.0+)
   - Configure app groups for data sharing between iOS and watchOS
   - Set up proper bundle identifiers and provisioning profiles

2. **Swift Package Structure**
   - Create `PulseCore` package for shared logic:
     - Math utilities for statistics (z-score calculation, rolling averages)
     - Feature extraction algorithms
     - Data models and common types
   - Create `PulseML` package for ML infrastructure:
     - Model wrapper protocols
     - Feature scaling utilities
     - Model versioning support

3. **HealthKit Configuration**
   - Add HealthKit capabilities and entitlements to both targets
   - Configure required permissions:
     - Heart Rate, HRV (SDNN), Resting HR
     - Respiratory Rate, Sleep Analysis
     - Apple Sleeping Wrist Temperature (Series 8+)
     - Workouts, Environmental Audio Exposure (optional)
   - Create mock data provider for simulator testing

4. **Core Architecture**
   - Set up MVVM architecture with SwiftUI
   - Create dependency injection container
   - Implement WatchConnectivity framework setup

## Week 2: Data ingestion & Storage
### Goals
- Implement comprehensive HealthKit data collection
- Build reliable local storage system

### Tasks
1. **HealthKit Service Layer**
   - Implement `HealthKitManager` with proper authorization flow
   - Create background observers:
     ```
     - HKObserverQuery for real-time heart rate updates
     - HKAnchoredObjectQuery for incremental data syncing
     - HKStatisticsCollectionQuery for historical data
     ```
   - Build query builders for each metric type
   - Implement data quality checks (skin contact, motion artifacts)

2. **Data Storage**
   - Design Core Data schema:
     ```
     - DailyMetrics entity (date, hrv_z, rhr_z, temp_z, etc.)
     - StressEvent entity (timestamp, confidence, features)
     - UserLabel entity (timestamp, stress_rating)
     - Settings entity (quiet_hours, thresholds)
     ```
   - Implement SwiftData models as alternative (iOS 17+)
   - Create data migration strategy
   - Build efficient query methods with proper indexing

3. **Background Tasks**
   - Set up `BGTaskScheduler` for nightly data processing
   - Implement `WKBackgroundRefreshScheduler` for watch updates
   - Create task priority system for battery optimization

## Week 3: Baselines & Recovery Algorithm
### Goals
- Implement statistical baseline calculations
- Build recovery scoring system

### Tasks
1. **Baseline Calculation Engine**
   - Implement 28-day rolling window statistics:
     - Median absolute deviation (MAD) for robust statistics
     - Exponential moving averages with decay
     - Outlier detection and removal
   - Create personalized baseline updater
   - Build cache system for performance

2. **Recovery Score Algorithm**
   - Implement z-score calculations for each metric:
     ```swift
     // HRV, RHR, Temperature, Respiratory Rate, Sleep Efficiency
     let weights = [0.35, 0.25, 0.20, 0.10, 0.10]
     ```
   - Create fusion algorithm with guardrails:
     - Minimum 3 valid metrics required
     - Confidence scoring based on data completeness
   - Build driver identification system

3. **UI Implementation**
   - Design and implement iPhone "Today" screen:
     - Recovery score visualization (0-100)
     - Key driver display with explanations
     - Action recommendations engine
   - Create basic Watch complication:
     - Circular gauge design
     - Text provider for different families

## Week 4: Real-time Stress Detection
### Goals
- Build real-time stress detection on Apple Watch
- Implement motion artifact handling

### Tasks
1. **Sensor Data Pipeline**
   - Set up CoreMotion integration:
     - Accelerometer and gyroscope at 50Hz
     - Motion feature extraction (jitter, posture)
   - Implement PPG-based HRV surrogate:
     - 30-60 second sliding windows
     - Inter-beat interval variance calculation
   - Create sensor fusion framework

2. **Stress Detection Algorithm**
   - Build heuristic threshold model:
     ```
     Features: [HR_elevation, HRV_drop, motion_jitter, posture_change]
     Thresholds: adaptive based on personal baseline
     ```
   - Implement two-signal validation rule
   - Add hysteresis to prevent flip-flopping
   - Create confidence scoring system

3. **Extended Runtime Sessions**
   - Implement `WKExtendedRuntimeSession`:
     - "Focus Session" mode for deliberate monitoring
     - Smart session management for battery
   - Create `HKWorkoutSession` wrapper:
     - Higher sensor sampling rates
     - Extended background runtime
   - Build session state machine

## Week 5: Core ML Integration
### Goals
- Replace heuristic model with ML
- Optimize for on-device inference

### Tasks
1. **Model Development**
   - Create training pipeline in Python:
     - Feature engineering (12-15 features)
     - Gradient boosted trees or 1D CNN
     - Cross-validation with user stratification
   - Implement model quantization:
     - 8-bit quantization for size
     - Performance benchmarking on device

2. **On-Watch Inference**
   - Build Core ML integration:
     - Model loading and versioning
     - Feature preprocessing pipeline
     - Batch inference for efficiency
   - Implement fallback to heuristic model
   - Create inference logging system

3. **Cooldown & Alert Logic**
   - Implement smart cooldown:
     - 10-minute minimum between alerts
     - Adaptive based on user response
   - Build context awareness:
     - Calendar integration (meetings)
     - Workout detection
     - Quiet hours respect

## Week 6: UX polish & Interactions
### Goals
- Create delightful user interactions
- Implement coaching features

### Tasks
1. **Breathing Exercise**
   - Design guided breathing interface:
     - Haptic feedback integration
     - Visual breathing guide
     - Progress tracking
   - Implement variations:
     - Box breathing (4-4-4-4)
     - 4-7-8 technique
     - Coherent breathing

2. **Notification System**
   - Create gentle stress alerts:
     - Haptic patterns design
     - Smart notification text
     - Quick actions integration
   - Build notification preferences:
     - Frequency controls
     - Context-based filtering
     - Do Not Disturb respect

3. **Visualizations**
   - Implement charts and graphs:
     - 7-day stress timeline
     - Recovery trend charts
     - Factor breakdown views
   - Add animations and transitions
   - Ensure accessibility compliance

4. **Accessibility**
   - VoiceOver optimization
   - Dynamic Type support
   - Reduce Motion support
   - Color blind friendly palettes

## Week 7: QA & field testing
### Goals
- Ensure reliability and accuracy
- Optimize battery performance

### Tasks
1. **Testing Infrastructure**
   - Set up comprehensive test suite:
     - Unit tests for algorithms
     - UI tests for critical flows
     - Performance tests
   - Create mock data generators
   - Build automated test scenarios

2. **Field Testing Protocol**
   - Recruit 10-20 beta testers
   - Implement in-app feedback:
     - 3x daily stress labels
     - Quick feedback forms
   - Create analytics dashboard
   - Set up crash reporting

3. **Battery Optimization**
   - Profile energy usage:
     - Sensor sampling rates
     - Background processing
     - ML inference frequency
   - Implement adaptive sampling
   - Create battery saver mode

4. **Bug Fixes & Iteration**
   - Address crash reports
   - Fix UI/UX issues
   - Tune algorithm thresholds
   - Optimize performance bottlenecks

## Week 8: Ship preparation
### Goals
- Prepare for App Store submission
- Create supporting materials

### Tasks
1. **App Store Requirements**
   - Create app metadata:
     - Compelling description
     - Keyword optimization
     - Category selection
   - Design screenshots:
     - iPhone (6.7", 6.1", 5.5")
     - Apple Watch Series 9
     - Feature highlights
   - Create preview video

2. **Privacy & Compliance**
   - Complete privacy nutrition label
   - Write comprehensive privacy policy
   - Implement data deletion flows
   - Add GDPR compliance features

3. **Export Features**
   - Implement PDF export:
     - Weekly/monthly reports
     - Professional formatting
     - Chart inclusion
   - Create CSV export:
     - Raw metrics data
     - Stress event logs
     - Configurable date ranges

4. **Documentation**
   - Write user guide
   - Create FAQ section
   - Build support infrastructure
   - Prepare press kit