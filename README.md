# **Synthetic Requirements Engineering: Evaluating LLM Capabilities for Large-Scale Dataset Construction**

Welcome to the official replication package for the **SIRA (Synthetic ISO Requirements Archive)** project.

SIRA is a novel, large-scale synthetic dataset of software requirements structurally aligned with the ISO/IEC 25010 quality model. This project explores the effectiveness of Advanced Large Language Models (LLMs) in generating high-quality, linguistically diverse, and task-relevant synthetic datasets to overcome data scarcity in Requirements Engineering (RE). By systematically injecting controlled semantic ambiguity and structural constraints, this repository provides a rigorous framework for generating and evaluating synthetic text data for machine learning tasks.

This repository is organized into multiple phases of our research pipeline.

---

## Phase 1: SIRA Prompt Generation Pipeline (Current Folder: `/Requirement Generation and Structural Variation`)

Generating high-quality synthetic requirements requires strict adherence to structural constraints and semantic ambiguity boundaries. To achieve this without relying on zero-shot inference, we designed a set of generalized prompt templates utilizing an expert persona, few-shot examples, and Chain-of-Thought (CoT) reasoning.

The `generate_prompts.py` script automatically instantiates these templates by combining:

1. **50 Software Projects** (Context and Domain)
2. **9 ISO/IEC 25010 Quality Classes** (Semantic Target)
3. **4 Stylistic Variations** (Short/Long and Ambiguous/Consistent)

### Repository Structure for Generation

- `generate_prompts.py`: The main Python script that orchestrates the prompt generation.
- `projects.json`: Contains the names and definitions of the 50 distinct software projects.
- `classes.json`: Contains the formal definitions of the ISO/IEC 25010 quality classes.
- `few_shot_samples.json`: Contains the human-validated few-shot examples utilized to guide the LLM's structural and stylistic tone.
- `/dist`: (Generated automatically) Contains the fully instantiated `.txt` prompt files organized by project and quality class, ready to be sent to the LLM API.
- `/data`: (Generated automatically) Empty template structure designated to store the raw responses returned by the LLMs.

### How it works

The script iterates through four primary stylistic variations:

- `PROMPT_SHORT_AMBIGUOUS` (10-20 words, 70-30% semantic overlap)
- `PROMPT_LONG_AMBIGUOUS` (25-50 words, 70-30% semantic overlap)
- `PROMPT_SHORT_CONSISTENT` (10-20 words, 0% overlap)
- `PROMPT_LONG_CONSISTENT` (25-50 words, 0% overlap)

For each combination of Project + ISO Class, it dynamically injects the appropriate `[PROJECT_NAME]`, `[CLASS_DEFINITION]`, and `[FEW_SHOT_EXAMPLES]`, producing a ready-to-execute `.txt` prompt.

### Execution

To replicate the prompt generation phase, simply run:

```bash
python generate_prompts.py
```

### Generated Prompt Examples

Below are two examples of what the fully instantiated `.txt` files look like inside the `/dist` folder after running the script:

**Example 1: Long & Ambiguous Variation**
_Filepath:_ `dist/project5/05_reliability_prompts/long_ambiguous.txt`

```text
You are a senior requirements engineer with deep expertise in ISO/IEC 25010. Your task is to generate 10 LONG and AMBIGUOUS requirements for a given software project and quality class.

Definition of "long and ambiguous":
- Long: one or two sentences, strictly containing between 25 and 50 words total.
- Ambiguous: lacks sufficient context or explicit boundary conditions, introducing controlled subjectivity. While it must primarily reflect the target quality class (70-80% of the core intent), its verbose but vague wording should allow it to be partially interpreted as a secondary class (20-30% overlap). Use subjective terms, unquantified scenarios, or open-ended exceptions.

Below are a few examples that illustrate the desired style. Use them as reference (few-shot) for tone, structure, and level of ambiguity.

1. The system must be available for use between 7:00AM and 11:59PM all days of the year.
2. In the event of a server crash, the system should automatically recover and restore all league data without significant data loss. The recovery process must be fast enough that users do not notice prolonged interruptions.
3. The system should maintain data integrity even when faced with common software defects. It is expected that recovery procedures will bring the system back to a consistent state in a reasonable timeframe.

Now, for the following project and quality class, generate 10 new requirements that follow the same long & ambiguous style.

Project name: Predictive Health Classifier for Wearable Devices
Project description: A supervised learning application embedded in wearable tech that classifies and predicts potential cardiac anomalies based on continuous biometric data streams.

Quality class (ISO/IEC 25010):
Class name: Reliability
Definition: This class determines the consistency with which a system performs its specified functions over a given period, characterized by faultless operation under normal conditions and dependable availability when required for use. It inherently includes the system's fault tolerance to operate as intended despite hardware or software defects, and its recoverability to rapidly re-establish a desired state and restore directly affected data following an unexpected interruption or failure.

Chain-of-Thought (think before you write):
1. Consider the project context: what are typical user interactions, system functions, or quality concerns?
2. Formulate the core intent based on the target Quality class.
3. Expand with context or conditions, but keep them vague. Inject controlled ambiguity so the text creates a slight semantic overlap with another class, while maintaining the primary class as dominant.
4. Verify constraint: Ensure each requirement is one or two sentences and strictly totals between 25 and 50 words.

Output format:

Requirements:
1.
2.
3.
...
10.

Ensure all requirements are directly related to the given quality class and the specific project.
```

**Example 2: Short & Consistent Variation**
_Filepath:_ `dist/project12/02_performance_efficiency_prompts/short_consistent.txt`

```text
You are a senior requirements engineer with deep expertise in ISO/IEC 25010. Your task is to generate 10 SHORT and CONSISTENT requirements for a given software project and quality class.

Definition of "short and consistent":
- Short: strictly a single sentence containing between 10 and 20 words.
- Consistent: presents a single unavoidable interpretation and is directly verifiable. It must have exclusive categorical alignment with the target class, meaning there is zero semantic overlap with other classes. Use precise language and clear conditions (e.g., specific actions, exact constraints, or logical/functional tests).

Below are a few examples that illustrate the desired style. Use them as reference (few-shot) for tone and structure.

1. The platform shall support 500 concurrent active calls.
2. Memory footprint shall not exceed 4 GB per node for 1 TB of data.
3. CPU utilization shall not exceed 70% during normal operation.

Now, for the following project and quality class, generate 10 new requirements that follow the same short & consistent style.

Project name: Next-Generation Graphics Rendering Software for Indie Studios
Project description: A desktop publishing and graphics application that provides cost-effective, high-fidelity 3D rendering and texturing tools tailored for independent video game developers.

Quality class (ISO/IEC 25010):
Class name: Performance Efficiency
Definition: This class evaluates the efficiency of a system in executing its functions within defined time and throughput parameters, ensuring that response times and processing rates meet required performance standards. It also accounts for the optimal utilization of varying hardware, software, and physical resources, alongside the system's overall capacity to uphold maximum operational limits and parameter thresholds under specified load conditions.

Chain-of-Thought (think before you write):
1. Consider the project context: what are typical user interactions, system functions, or quality concerns?
2. Formulate the requirement with absolute precision, ensuring it aligns exclusively with the target class without any semantic ambiguity.
3. Verify constraint: Ensure each requirement is exactly one sentence and strictly between 10 and 20 words long.

Output format:

Requirements:
1.
2.
3.
...
10.

Ensure all requirements are directly related to the given quality class and the specific project.
```

# Complete list of software projects and their domains

| ID | Project Name | Domain |
|----|--------------|--------|
| 1 | Reinforcement Learning Agent for Supply Chain Logistics | Logistics |
| 2 | Ambient Intelligence Smart Home Controller | Consumer IoT |
| 3 | Autonomous Navigation Engine for Agricultural Drones | Agriculture |
| 4 | Predictive Health Classifier for Wearable Devices | Healthcare |
| 5 | Multilingual Machine Translation Service for Legal Documents | Legal |
| 6 | Real-Time Speech Recognition Kiosk for International Airports | Travel/Aviation |
| 7 | Corporate Financial Report Information Extraction Engine | Finance |
| 8 | Automated Customer Support Question Answering Bot | Customer Service |
| 9 | Electronic Trading Platform for Carbon Credits | Finance/Environmental |
| 10 | Distributed Multimedia Platform for Remote Education | Education |
| 11 | Cloud-Based Content Management System for Digital Publishers | Media/Publishing |
| 12 | Next-Generation Graphics Rendering Software for Indie Studios | Entertainment/Gaming |
| 13 | Distributed Cloud Computing Engine for Bioinformatics | Bioinformatics |
| 14 | Embedded System Firmware for Automotive Braking | Automotive |
| 15 | Quantum Cryptography Key Distribution Network | Defense/Cybersecurity |
| 16 | High-Availability Server Cluster for E-Commerce Checkout | E-Commerce |
| 17 | Real-Time Video Processing Pipeline for Security Feeds | Security/Surveillance |
| 18 | Medical Image Retrieval System for Radiology | Healthcare |
| 19 | Cryptographic Data Processing Vault for Banking | Banking |
| 20 | Streaming Data Analytics Engine for IoT Devices | Industrial IoT |
| 21 | Semantic Search Algorithm for Academic Papers | Academia/Research |
| 22 | Distributed NoSQL Database System for Social Networks | Social Media |
| 23 | Digital Identity and Credential Wallet for e-Government Services | Government/Civic Tech |
| 24 | Retail Analytics and Feature Learning Dashboard | Retail |
| 25 | Mechatronics Control System for Robotic Assembly | Manufacturing |
| 26 | Real-Time Computing Kernel for Aerospace Telemetry | Aerospace |
| 27 | Smart City Civil Engineering Simulation Framework | Civil Engineering |
| 28 | Blockchain-Based Smart Contract Validator | Web3/Blockchain |
| 29 | Semantic Web Knowledge Graph Platform | Information Architecture |
| 30 | Decentralized Web Hosting and Filestore Network | Internet Infrastructure |
| 31 | Web Accessibility Compliance Checker | Web Compliance |
| 32 | Integrated Development Environment for IoT Firmware | Developer Tools |
| 33 | Automated Computer Debugging and Heuristic Analysis Tool | Enterprise Software |
| 34 | Mathematical Interpolation Library for Weather Forecasting | Meteorology |
| 35 | Secure Pattern Matching Engine for Antivirus Scanning | Cybersecurity |
| 36 | Homeland Security Event Projection System | Government defense |
| 37 | Real Estate PDA Assistant | Real estate |
| 38 | Nursing Clinical Scheduling System | Healthcare |
| 39 | Credit Card Holder Services Portal | Financial |
| 40 | Recycled Auto Parts Inventory System | Automotive retail |
| 41 | Enterprise DBMS and Server Management System | IT Infrastructure |
| 42 | Inventory Quantity Adjustment System | Warehouse and Logistics |
| 43 | Movie Subscription and Prepaid Card System | Entertainment retail |
| 44 | Sales Lead Evaluation and Assignment Platform | Corporate sales |
| 45 | Tactical Ship Simulation Game | Gaming |
| 46 | Teleservices Call Management Platform | Telecommunications |
| 47 | City of Chicago Municipal Development Framework | Government |
| 48 | Corporate Reporting and Management Dashboard | Business Intelligence |
| 49 | Fantasy League Management Platform | Entertainment |
| 50 | RFS Financial Budgeting System | Finance |
