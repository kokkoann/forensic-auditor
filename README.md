# 🐕 LedgerHound

### AI-Assisted Forensic Auditor for Financial Fraud Investigation

> **Follow the money. Find the evidence. Keep the human in control.**

LedgerHound is a forensic auditing platform designed to help investigators detect suspicious financial activity, trace money flows, and organize evidence from financial records.

Instead of asking an AI model to arbitrarily decide whether a company is fraudulent, LedgerHound separates **deterministic detection, financial analysis, evidence generation, and AI-assisted investigation** into different layers.

The goal is simple:

**Reduce the time investigators spend searching for suspicious transactions, without replacing their professional judgment.**

---

## 🎯 The Problem

Financial fraud investigations involve large amounts of fragmented information:

* Invoices
* Transaction records
* Supplier information
* Tax identifiers (RFCs)
* Government blacklists
* Repeated payments
* Abnormal transaction patterns
* Money flows between multiple entities

Finding useful evidence manually can require investigators to inspect thousands of records and reconstruct relationships transaction by transaction.

At the same time, a simple anomaly detector is not enough.

A duplicated payment may be an accounting error.
An unusual transaction may be legitimate.
A suspicious supplier does not automatically prove fraud.

**Detection is not the same as judgment.**

LedgerHound was built around that principle.

---

# 💡 Our Solution

LedgerHound acts as an **investigative copilot for forensic auditors**.

The platform automatically processes financial datasets and searches for predefined indicators of suspicious activity.

It can:

🔎 Identify entities appearing in SAT Article 69-B records.

🔁 Detect duplicated transactions.

⚠️ Identify anomalous financial movements.

💸 Reconstruct money trails between entities.

📊 Calculate and organize risk indicators.

📁 Build structured evidence associated with each finding.

🤖 Allow investigators to explore the resulting report through an AI assistant.

Instead of making accusations automatically, LedgerHound helps answer a more useful question:

> **"What should the investigator look at first, and what evidence supports it?"**

---

# 🧠 How LedgerHound Works

LedgerHound uses a hybrid architecture where traditional software performs the heavy financial analysis and an LLM is used only where language reasoning provides additional value.

```text
                    ┌───────────────────────┐
                    │   Investigator / User │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │    Upload Document    │
                    │    CSV / Financial    │
                    │        Records        │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │        Parser         │
                    │ Normalize & structure │
                    │         data          │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │      Classifier       │
                    │ Identify document and │
                    │      data types       │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │        Router         │
                    │ Select the required   │
                    │      detectors        │
                    └───────────┬───────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
       ┌────────────┐    ┌────────────┐    ┌────────────┐
       │ SAT 69-B   │    │ Duplicate  │    │  Anomaly   │
       │ Detector   │    │ Detector   │    │ Detector   │
       └─────┬──────┘    └─────┬──────┘    └─────┬──────┘
             │                 │                 │
             └─────────────────┼─────────────────┘
                               │
                               ▼
                    ┌───────────────────────┐
                    │     Money Trail       │
                    │    Graph Analysis     │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │    Evidence Engine    │
                    │ Findings + amounts +  │
                    │      traceability     │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │    Forensic Report    │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │     AI Assistant      │
                    │ Ask questions about   │
                    │     the evidence      │
                    └───────────────────────┘
```

---

# ⚙️ Analysis Pipeline

## 1. Document Ingestion

The investigator uploads the financial information that will be analyzed.

LedgerHound prepares the file for processing and validates its structure before running forensic detectors.

```text
Raw File
   ↓
Validation
   ↓
Parsing
   ↓
Normalization
   ↓
Structured Records
```

---

## 2. Parser

The parser transforms raw information into standardized records that the rest of the application can understand.

Typical fields may include:

```text
RFC
Company
Transaction ID
Sender
Receiver
Amount
Date
Invoice ID
Payment Reference
```

This prevents each detector from having to independently understand the original document.

---

## 3. Classifier

Once the document has been parsed, LedgerHound determines what type of information is available.

This allows the system to identify which analyses can actually be performed on the uploaded dataset.

---

## 4. Router

The Router coordinates the forensic analysis.

Instead of sending the entire dataset to an LLM, the Router decides which specialized detector should process each type of information.

```python
Document
   │
   ▼
 Router
   │
   ├── SAT 69-B Detector
   ├── Duplicate Detector
   ├── Anomaly Detector
   └── Money Trail Analysis
```

This modular approach makes LedgerHound easier to extend and reduces unnecessary AI processing.

---

# 🔎 Detection Modules

## SAT Article 69-B Detection

LedgerHound can cross-reference RFCs found in financial records against information derived from the SAT Article 69-B dataset.

This allows investigators to quickly identify transactions involving entities that require additional scrutiny.

The result becomes an **investigative signal**, not an automatic declaration of fraud.

---

## 🔁 Duplicate Detection

The system searches for repeated or potentially duplicated financial operations.

Possible indicators include combinations of:

```text
same sender
+ same receiver
+ same amount
+ similar timestamp
+ same invoice/reference
```

Detected duplicates are added to the evidence associated with the case.

---

## ⚠️ Anomaly Detection

LedgerHound identifies transactions that deviate from the expected behavior of the dataset.

Examples may include:

* Unusually large transactions
* Abnormal transaction frequency
* Irregular relationships between entities
* Concentration of payments
* Unexpected transaction patterns

An anomaly is treated as a **lead for investigation**, not proof of wrongdoing.

---

# 💸 Money Trail

Financial fraud rarely exists as a single isolated transaction.

The **Money Trail** module reconstructs relationships between entities as a graph.

```text
Company A
   │
   │ $500,000
   ▼
Company B
   │
   │ $480,000
   ▼
Company C
   │
   │ $450,000
   ▼
Company A
```

This representation can help investigators identify patterns such as:

* Circular money flows
* Intermediary entities
* Concentrated payment networks
* Suspicious chains of transactions
* Potential round-tripping behavior

The frontend can visualize these relationships interactively so investigators can follow the movement of money instead of manually reconstructing it from rows in a spreadsheet.

---

# 📁 Evidence-First Design

One of LedgerHound's core principles is:

> **No finding without evidence.**

Every relevant detection should be associated with the underlying information that triggered it.

For example:

```json
{
  "finding": "POTENTIAL_DUPLICATE",
  "severity": "HIGH",
  "transactions": [
    "TX-10482",
    "TX-10491"
  ],
  "amount": 250000,
  "reason": "Same sender, receiver and amount detected.",
  "evidence_source": "uploaded_transactions.csv"
}
```

This architecture makes findings easier for investigators to verify independently.

---

# 📊 Risk Prioritization

LedgerHound organizes findings according to their relevance.

```text
HIGH
MEDIUM
LOW
```

The objective of the risk score is **prioritization**, not conviction.

A HIGH risk indicator means:

> "This deserves the investigator's attention."

It does **not** mean:

> "This company committed fraud."

This distinction is fundamental to LedgerHound.

---

# 🤖 Role of Artificial Intelligence

LedgerHound intentionally does **not** send raw financial datasets directly to an LLM and ask:

> "Is this company fraudulent?"

Large Language Models are powerful reasoning and communication tools, but they should not arbitrarily determine guilt from financial records.

Instead, LedgerHound first performs deterministic and statistical analysis.

```text
Financial Data
      ↓
Detectors
      ↓
Structured Findings
      ↓
Evidence
      ↓
Forensic Report
      ↓
LLM
```

The AI assistant operates primarily over the **structured results of the investigation**.

Investigators can then ask questions such as:

```text
Why was this transaction marked as HIGH risk?

Which entities are connected to this RFC?

What evidence supports this finding?

Show me the suspicious money trail.

Which transactions were detected as duplicates?

Summarize the most important findings in this case.
```

This architecture reduces the amount of irrelevant information that needs to be processed by the LLM while keeping the underlying evidence accessible.

---

# 🧑‍⚖️ Human-in-the-Loop

LedgerHound does not attempt to replace forensic investigators.

It is designed to amplify them.

```text
              LedgerHound

                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼

     Automation          Human Judgment

 Detect patterns       Interpret context
 Search records        Validate evidence
 Trace money           Form hypotheses
 Prioritize leads      Make conclusions
```

The system finds signals.

**The investigator decides what they mean.**

This helps reduce two important risks:

### False positives

Legitimate organizations should not be accused simply because an algorithm detected an unusual transaction.

### False negatives

Sophisticated fraud should not go unnoticed simply because it does not match one predefined rule.

LedgerHound therefore combines automated detection with professional human judgment.

---

# 🖥️ Investigation Interface

The frontend is designed around an investigator's workflow.

```text
┌───────────────────────────────────────────────────────────────┐
│ LEDGERHOUND                         RFC: ABC123456XXX         │
├──────────────┬────────────────────────────────────────────────┤
│              │                                                │
│ CASE HISTORY │  Search RFC, company, transaction...          │
│              │                                                │
│ + New Case   │  [SAT-69B] [Anomalies] [Duplicates]          │
│              │  [Money Trail]                                │
│ Case #004    │                                                │
│ Case #003    │  RISK SCORE              EVIDENCE             │
│ Case #002    │                                                │
│              │  HIGH                     12 findings          │
│              │                                                │
│              │  ──────────────────────────────────────────    │
│              │                                                │
│              │              MONEY TRAIL                       │
│              │                                                │
│              │        A ─────► B ─────► C                    │
│              │        ▲               │                       │
│              │        └───────────────┘                       │
│              │                                                │
├──────────────┴────────────────────────────────────────────────┤
│ Ask LedgerHound about this investigation...                  │
└───────────────────────────────────────────────────────────────┘
```

The interface allows investigators to move between **findings, evidence, transactions and money trails** without losing the context of the investigation.

---

# 🏗️ Architecture

A simplified representation of the application:

```text
┌───────────────────────────┐
│         Frontend          │
│   Investigation Dashboard│
└─────────────┬─────────────┘
              │
              │ HTTP / API
              ▼
┌───────────────────────────┐
│          Backend          │
│          FastAPI          │
└─────────────┬─────────────┘
              │
              ▼
┌───────────────────────────┐
│          Router           │
└─────────────┬─────────────┘
              │
     ┌────────┼────────┐
     ▼        ▼        ▼
   SAT      Duplicate  Anomaly
   69-B     Detection  Detection
     │        │        │
     └────────┼────────┘
              ▼
       Evidence Engine
              │
              ▼
        Money Trail
              │
              ▼
       Forensic Report
              │
              ▼
        AI Assistant
```

---

# 🛠️ Technology Stack

### Backend

* Python
* FastAPI
* Uvicorn
* Pandas
* Data processing and forensic detection modules

### AI Layer

* Large Language Model API
* Structured forensic context
* Report-based conversational assistant

### Data Analysis

* Rule-based detection
* Statistical anomaly detection
* Duplicate detection
* Graph-based money-flow analysis

### Frontend

* HTML
* CSS
* JavaScript
* Interactive forensic dashboard
* Money Trail visualization

### Data Sources

LedgerHound was designed around publicly available financial and fraud-related resources, including:

* SAT Article 69-B information
* CFDI-related financial structures
* Synthetic financial transaction datasets
* AML-style money-flow patterns

---

# 📂 Project Structure

A simplified representation of the repository:

```text
LedgerHound/
│
├── backend/
│   │
│   ├── main.py
│   │
│   ├── parser/
│   │   └── ...
│   │
│   ├── classifier/
│   │   └── ...
│   │
│   ├── router/
│   │   └── ...
│   │
│   ├── detectors/
│   │   ├── sat69b.py
│   │   ├── duplicates.py
│   │   └── anomalies.py
│   │
│   ├── money_trail/
│   │   └── ...
│   │
│   ├── evidence/
│   │   └── ...
│   │
│   ├── report/
│   │   └── ...
│   │
│   └── ai/
│       └── ...
│
├── frontend/
│   │
│   ├── index.html
│   ├── styles/
│   ├── scripts/
│   └── assets/
│
├── datasets/
│   ├── sat_69b/
│   └── sample_transactions/
│
├── tests/
│
├── requirements.txt
├── .gitigno
```
