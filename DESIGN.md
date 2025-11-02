# Dashboard Design Overview

## 🎨 CIMB Theme

**Primary Colors:**
- CIMB Red: #BB0A21 (Brand color)
- CIMB Red Dark: #9A0819 (Gradients)
- White: #FFFFFF (Background)
- Light Gray: #F5F5F5 (Secondary background)

## 📱 Dashboard Layout

### 1. Header
```
┌─────────────────────────────────────────────────────────┐
│  CIMB | Anti-Scam Dashboard          [🧪 Mock Mode]    │
│  (Red gradient background with white text)              │
└─────────────────────────────────────────────────────────┘
```

### 2. Upload Section
```
┌─────────────────────────────────────────────────────────┐
│         Upload Transaction Data                         │
│  Upload an Excel file containing transaction records    │
│                                                          │
│  ┌────────────────────────────────────────────┐        │
│  │  📁  Choose Excel File                      │        │
│  └────────────────────────────────────────────┘        │
│                                                          │
│      [Analyze Transactions]                             │
└─────────────────────────────────────────────────────────┘
```

### 3. Summary Cards (After Upload)
```
┌──────────┐  ┌──────────┐  ┌──────────┐
│ 📊       │  │ 🚨       │  │ ✓        │
│ 20       │  │ 8        │  │ 12       │
│ Total    │  │ Fraud    │  │ Legit    │
└──────────┘  └──────────┘  └──────────┘
   (White)    (Red gradient)   (White)
```

### 4. Fraudulent Transactions Table
```
┌─────────────────────────────────────────────────────────┐
│  🚨 Fraudulent Transactions                             │
│  Click on any transaction to view detailed analysis     │
│                                                          │
│  ID  Amount    Duration  Logins  Balance  Age  Score   │
│  ──────────────────────────────────────────────────── │
│  1   7,500.00    5s       5     8,000    22   [85%]   │
│  2   9,800.00    8s       4    10,000    28   [78%]   │
│  ... (clickable rows)                                   │
└─────────────────────────────────────────────────────────┘
```

### 5. Detail Modal (On Click)
```
┌───────────────────────────────────────────────────────┐
│  Fraud Analysis                                   [×] │
│  (Red header background)                              │
├───────────────────────────────────────────────────────┤
│                                                       │
│  Transaction Details                                  │
│  ┌─────────────┬─────────────┐                      │
│  │ ID: 1       │ Amount:     │                      │
│  │             │ RM 7,500.00 │                      │
│  │ Duration:   │ Logins: 5   │                      │
│  │ 5s          │             │                      │
│  └─────────────┴─────────────┘                      │
│                                                       │
│  Risk Score: [85%] High Risk                         │
│                                                       │
│  AI Analysis                                          │
│  ┌─────────────────────────────────────────────┐    │
│  │ 🚨 Fraud Alert Analysis                      │    │
│  │                                               │    │
│  │ This transaction has been flagged due to:    │    │
│  │ 1. Unusually high transaction amount...      │    │
│  │ 2. Excessive login attempts...               │    │
│  │ 3. Very short transaction duration...        │    │
│  └─────────────────────────────────────────────┘    │
└───────────────────────────────────────────────────────┘
```

## 🎯 Key Features

### Color-Coded Risk Levels
- 🔴 **Critical** (80-100%): Dark Red #BB0A21
- 🟠 **High** (60-79%): Light Red #E63946
- 🟡 **Medium** (40-59%): Orange #F77F00
- 🟢 **Low** (0-39%): Green #06A77D

### Interactive Elements
- Hover effects on cards and table rows
- Smooth transitions and animations
- Modal popup for detailed analysis
- Loading spinners during processing
- Responsive design for mobile/desktop

### Mock Mode Indicators
- Badge showing "🧪 Mock Mode" when APIs not configured
- Banner at bottom of results showing mock status
- Automatic fallback without errors

## 📊 Data Flow

1. User uploads Excel file
2. Backend validates required columns
3. Each transaction sent to ML API (or mock)
4. Fraudulent transactions filtered and displayed
5. User clicks transaction → AI explanation generated
6. Results shown in modal with formatted analysis

## 🎭 User Experience

- **Minimalistic**: Clean white backgrounds, ample spacing
- **Professional**: CIMB brand colors throughout
- **Intuitive**: Clear labels, icons, and visual hierarchy
- **Responsive**: Works on phones, tablets, and desktops
- **Fast**: Optimistic UI updates, loading indicators
- **Forgiving**: Mock mode for demo without API keys
