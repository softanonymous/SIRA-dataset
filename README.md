# **Synthetic Requirements Engineering: Evaluating LLM Capabilities for Large-Scale Dataset Construction**

Welcome to the official replication package for the **SIRA (Synthetic ISO Requirements Archive)** project.

SIRA is a novel, large-scale synthetic dataset of software requirements structurally aligned with the ISO/IEC 25010 quality model. This project explores the effectiveness of Advanced Large Language Models (LLMs) in generating high-quality, linguistically diverse, and task-relevant synthetic datasets to overcome data scarcity in Requirements Engineering (RE). By systematically injecting controlled semantic ambiguity and structural constraints, this repository provides a rigorous framework for generating and evaluating synthetic text data for machine learning tasks.

This repository is organized into multiple phases of our research pipeline.

---

## Phase 1: SIRA Prompt Generation Pipeline (Folder: `/phase1`)

Generating high-quality synthetic requirements requires strict adherence to structural constraints and semantic ambiguity boundaries. To achieve this without relying on zero-shot inference, we designed a set of generalized prompt templates utilizing an expert persona, few-shot examples, and Chain-of-Thought (CoT) reasoning.

The `generate_prompts.py` script automatically instantiates these templates by combining:

1. **50 Software Projects** (Context and Domain)
2. **9 ISO/IEC 25010 Quality Classes** (Semantic Target)
3. **4 Stylistic Variations** (Short/Long and Ambiguous/Consistent)

### Repository Structure for Generation, Curation, and Evaluation

- `generate_prompts.py`: The main Python script that orchestrates the prompt generation.
- `deduplication.py`: Handles the automated data curation phase. It sequentially executes exact string deduplication followed by semantic deduplication using Sentence-BERT (SBERT) embeddings and a 0.8 cosine similarity threshold, systematically filtering out redundant generated requirements.
- `evaluation.py`: Computes the linguistic and semantic diversity metrics of the final dataset. It calculates the Vocabulary Size, Average Pairwise Similarity (APS), and Inter-N-gram Frequency (INGF-3 and INGF-4) to benchmark the synthetic dataset against real-world baselines like PROMISE and ReSpaN.
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

---

## Complete list of software projects and their domains

| ID  | Project Name                                                     | Domain                   |
| --- | ---------------------------------------------------------------- | ------------------------ |
| 1   | Reinforcement Learning Agent for Supply Chain Logistics          | Logistics                |
| 2   | Ambient Intelligence Smart Home Controller                       | Consumer IoT             |
| 3   | Autonomous Navigation Engine for Agricultural Drones             | Agriculture              |
| 4   | Predictive Health Classifier for Wearable Devices                | Healthcare               |
| 5   | Multilingual Machine Translation Service for Legal Documents     | Legal                    |
| 6   | Real-Time Speech Recognition Kiosk for International Airports    | Travel/Aviation          |
| 7   | Corporate Financial Report Information Extraction Engine         | Finance                  |
| 8   | Automated Customer Support Question Answering Bot                | Customer Service         |
| 9   | Electronic Trading Platform for Carbon Credits                   | Finance/Environmental    |
| 10  | Distributed Multimedia Platform for Remote Education             | Education                |
| 11  | Cloud-Based Content Management System for Digital Publishers     | Media/Publishing         |
| 12  | Next-Generation Graphics Rendering Software for Indie Studios    | Entertainment/Gaming     |
| 13  | Distributed Cloud Computing Engine for Bioinformatics            | Bioinformatics           |
| 14  | Embedded System Firmware for Automotive Braking                  | Automotive               |
| 15  | Quantum Cryptography Key Distribution Network                    | Defense/Cybersecurity    |
| 16  | High-Availability Server Cluster for E-Commerce Checkout         | E-Commerce               |
| 17  | Real-Time Video Processing Pipeline for Security Feeds           | Security/Surveillance    |
| 18  | Medical Image Retrieval System for Radiology                     | Healthcare               |
| 19  | Cryptographic Data Processing Vault for Banking                  | Banking                  |
| 20  | Streaming Data Analytics Engine for IoT Devices                  | Industrial IoT           |
| 21  | Semantic Search Algorithm for Academic Papers                    | Academia/Research        |
| 22  | Distributed NoSQL Database System for Social Networks            | Social Media             |
| 23  | Digital Identity and Credential Wallet for e-Government Services | Government/Civic Tech    |
| 24  | Retail Analytics and Feature Learning Dashboard                  | Retail                   |
| 25  | Mechatronics Control System for Robotic Assembly                 | Manufacturing            |
| 26  | Real-Time Computing Kernel for Aerospace Telemetry               | Aerospace                |
| 27  | Smart City Civil Engineering Simulation Framework                | Civil Engineering        |
| 28  | Blockchain-Based Smart Contract Validator                        | Web3/Blockchain          |
| 29  | Semantic Web Knowledge Graph Platform                            | Information Architecture |
| 30  | Decentralized Web Hosting and Filestore Network                  | Internet Infrastructure  |
| 31  | Web Accessibility Compliance Checker                             | Web Compliance           |
| 32  | Integrated Development Environment for IoT Firmware              | Developer Tools          |
| 33  | Automated Computer Debugging and Heuristic Analysis Tool         | Enterprise Software      |
| 34  | Mathematical Interpolation Library for Weather Forecasting       | Meteorology              |
| 35  | Secure Pattern Matching Engine for Antivirus Scanning            | Cybersecurity            |
| 36  | Homeland Security Event Projection System                        | Government defense       |
| 37  | Real Estate PDA Assistant                                        | Real estate              |
| 38  | Nursing Clinical Scheduling System                               | Healthcare               |
| 39  | Credit Card Holder Services Portal                               | Financial                |
| 40  | Recycled Auto Parts Inventory System                             | Automotive retail        |
| 41  | Enterprise DBMS and Server Management System                     | IT Infrastructure        |
| 42  | Inventory Quantity Adjustment System                             | Warehouse and Logistics  |
| 43  | Movie Subscription and Prepaid Card System                       | Entertainment retail     |
| 44  | Sales Lead Evaluation and Assignment Platform                    | Corporate sales          |
| 45  | Tactical Ship Simulation Game                                    | Gaming                   |
| 46  | Teleservices Call Management Platform                            | Telecommunications       |
| 47  | City of Chicago Municipal Development Framework                  | Government               |
| 48  | Corporate Reporting and Management Dashboard                     | Business Intelligence    |
| 49  | Fantasy League Management Platform                               | Entertainment            |
| 50  | RFS Financial Budgeting System                                   | Finance                  |

---

## Phase 2: Full Prompt Catalog (Folder: `/phase2`)

To ensure full transparency and reproducibility of our methodology, below is the complete sequence of prompts utilized during the dataset construction and validation phases.

### PROMPT 1: Class definition (Persona + Chain-of-Thought + Contextual Prompting)

```text
Act as a Senior Software Requirements Engineer and Taxonomy Expert specialized in generating high-quality training datasets for Large Language Models.

TASK:
Analyze the provided list of ISO 25010 software quality characteristics and their respective sub-characteristics. Your goal is to synthesize these into highly precise, cohesive, and distinguishable class definitions. These definitions will act as the ground truth to classify complex and potentially ambiguous software requirements, so they must seamlessly encapsulate the entire scope of the characteristic and its sub-components.

INPUT DATA:
1. Functional Suitability
This characteristic represents the degree to which a product or system provides functions that meet stated and implied needs when used under specified conditions. This characteristic is composed of the following sub-characteristics:
- Functional completeness - Degree to which the set of functions covers all the specified tasks and intended users' objectives.
- Functional correctness - Degree to which a product or system provides accurate results when used by intended users.
- Functional appropriateness - Degree to which the functions facilitate the accomplishment of specified tasks and objectives.

2. Performance Efficiency
This characteristic represents the degree to which a product performs its functions within specified time and throughput parameters and is efficient in the use of resources (such as CPU, memory, storage, network devices, energy, materials...) under specified conditions. This characteristic is composed of the following sub-characteristics:
- Time behaviour - Degree to which the response time and throughput rates of a product or system, when performing its functions, meet requirements.
- Resource utilization - Degree to which the amounts and types of resources used by a product or system, when performing its functions, meet requirements.
- Capacity - Degree to which the maximum limits of a product or system parameter meet requirements.

3. Compatibility
Degree to which a product, system or component can exchange information with other products, systems or components, and/or perform its required functions while sharing the same common environment and resources. This characteristic is composed of the following sub-characteristics:
- Co-existence - Degree to which a product can perform its required functions efficiently while sharing a common environment and resources with other products, without detrimental impact on any other product.
- Interoperability - Degree to which a system, product or component can exchange information with other products and mutually use the information that has been exchanged.

4. Interaction Capability
Degree to which a product or system can be interacted with by specified users to exchange information ia the user interfaceto complete specific tasks in a variety of contexts of use. This characteristic is composed of the following sub-characteristics:
- Appropriateness recognizability - Degree to which users can recognize whether a product or system is appropriate for their needs.
- Learnability - Degree to which the functions of a product or system can be learnt to be used by specified users within a specified amount of time.
- Operability - Degree to which a product or system has attributes that make it easy to operate and control.
- User error protection. Degree to which a system prevents users against operation errors.
- User engagement - Degree to which a user interface presents functions and information in an inviting and motivating manner encouraging continued interaction.
- Inclusivity - Degree to which a product or system can be used by people of various backgrounds (such as people of various ages, abilities, cultures, ethnicities, languages, genders, economic situations, etc.).
- User assistance - Degree to which a product can be used by people with the widest range of characteristics and capabilities to achieve specified goals in a specified context of use.
- Self-descriptiveness - Degree to wich a product presents appropriate information, where needed by the user, to make its capabilities and use immediately obvious to the user without excessive interactions with a product or other resources (such as user documentation, help desks or other users).

5. Reliability
Degree to which a system, product or component performs specified functions under specified conditions for a specified period of time. This characteristic is composed of the following sub-characteristics:
- Faultlessness - Degree to which a system, product or component performs specified functions without fault under normal operation.
- Availability - Degree to which a system, product or component is operational and accessible when required for use.
- Fault tolerance - Degree to which a system, product or component operates as intended despite the presence of hardware or software faults.
- Recoverability - Degree to which, in the event of an interruption or a failure, a product or system can recover the data directly affected and re-establish the desired state of the system.

6. Security
Degree to which a product or system defends against attack patterns by malicious actos and protects information and data so that persons or other products or systems have the degree of data access appropriate to their types and levels of authorization. This characteristic is composed of the following sub-characteristics:
- Confidentiality - Degree to which a product or system ensures that data are accessible only to those authorized to have access.
- Integrity - Degree to which a system, product or component ensures that the state of its system and data are protected from unauthorized modification or deletion either by malicious action or computer error.
- Non-repudiation - Degree to which actions or events can be proven to have taken place so that the events or actions cannot be repudiated later.
- Accountability - Degree to which the actions of an entity can be traced uniquely to the entity.
- Authenticity - Degree to which the identity of a subject or resource can be proved to be the one claimed.
- Resistance - Degree to which the product or system sustains operations while under attack from a malicious actor.

7. Maintainability
This characteristic represents the degree of effectiveness and efficiency with which a product or system can be modified to improve it, correct it or adapt it to changes in environment, and in requirements. This characteristic is composed of the following sub-characteristics:
- Modularity - Degree to which a system or computer program is composed of discrete components such that a change to one component has minimal impact on other components.
- Reusability - Degree to which a product can be used as an asset in more than one system, or in building other assets.
- Analysability - Degree of effectiveness and efficiency with which it is possible to assess the impact on a product or system of an intended change to one or more of its parts, to diagnose a product for deficiencies or causes of failures, or to identify parts to be modified.
- Modifiability - Degree to which a product or system can be effectively and efficiently modified without introducing defects or degrading existing product quality.
- Testability - Degree of effectiveness and efficiency with which test criteria can be established for a system, product or component and tests can be performed to determine whether those criteria have been met.

8. Flexibility
Degree to which a product can be adapted to changes in its requirements, contexts of use or sys tem environment. This characteristic is composed of the following sub-characteristics:
- Adaptability - Degree to which a product or system can effectively and efficiently be adapted for or transferred to different hardware, software or other operational or usage environments.
- Scalability - Degree to which a product can handle growing or shrinking workloads or to adapt its capacity to handle variability.
- Installability - Degree of effectiveness and efficiency with which a product or system can be successfully installed and/or uninstalled in a specified environment.
- Replaceability - Degree to which a product can replace another specified software product for the same purpose in the same environment.

9. Safety
This characteristic represents the degree to which a product under defined conditions to avoid a state in which human life, health, property, or the environment is endangered. This characteristic is composed of the following sub-characteristics:
- Operational constraint - Degree to which a product or system constrains its operation to within safe parameters or states when encountering operational hazard.
- Risk identification - Degree to which a product can identify a course of events or operations that can expose life, property or environment to unacceptable risk.
- Fail safe - Degree to which a product can automatically place itself in a safe operating mode, or to revert to a safe condition in the event of a failure.
- Hazard warning - Degree to which a product or system provides warnings of unacceptable risks to operations or internal controls so that they can react in sufficient time to sustain safe operations.
- Safe integration - Degree to which a product can maintain safety during and after integration with one or more components.

INSTRUCTIONS:

Step 1 — Core Boundary Analysis (Chain of Thought)
For each of the 9 main characteristics, analyze its core definition to establish a strict boundary that differentiates it from the other 8 classes.

Step 2 — Semantic Keyword Integration (Chain of Thought)
Analyze the sub-characteristics belonging to each main class. Extract their core semantic concepts (e.g., for Maintainability: modularity, reusability, testability, etc.). Do not treat them as a list, but as building blocks of a broader concept.

Step 3 — Definition Synthesis
Draft a comprehensive, fluid paragraph for the "class_definition" field.
- The definition must be composed of complete, well-structured sentences.
- It must state the main purpose of the characteristic and seamlessly weave the specific concepts, keywords, and constraints of ALL its sub-characteristics into the natural prose.
- Do NOT use bullet points, and do NOT explicitly write phrases like "The keywords are..." or "This includes sub-characteristics such as...".
- The resulting description must make the full scope of the class immediately obvious and easily distinguishable for a machine learning classifier, capturing both the overarching goal and the nuanced sub-traits.

OUTPUT FORMAT:
Provide the output strictly as a JSON array of objects. Do not include any conversational filler.

[
    {
        "class_name": "Functional Suitability",
        "class_definition": "..."
    },
    {
        "class_name": "Performance Efficiency",
        "class_definition": "..."
    }
]
```

### PROMPT 2: ISO Classes Validation (Persona + Self-Reflection)

```text
Act as an Expert Quality Assurance Specialist for Software Engineering Datasets. Your task is to review a set of automatically generated class definitions for the ISO 25010 software quality characteristics, perform a critical self-reflection, and refine them to ensure they are optimal for training a Large Language Model classifier.

INPUT DATA 1: OFFICIAL ISO 25010 STANDARD
[Insert the official list of the 9 ISO characteristics and their sub-characteristics here]

INPUT DATA 2: GENERATED DEFINITIONS
[Insert the JSON array of the 9 generated class definitions from the previous prompt here]

VALIDATION AND SELF-REFLECTION STEPS:
Please critically analyze the generated definitions against the official standard using the following criteria:

1. Accuracy and Fidelity: Does the generated definition accurately reflect the core intent of the official ISO characteristic without hallucinating outside concepts?
2. Sub-characteristic Integration: Does the paragraph organically and implicitly weave in the concepts of ALL its associated sub-characteristics without explicitly listing them or using phrases like "This includes..." or "Keywords are..."?
3. Boundary Differentiation: Are the boundaries between the 9 classes stark and clear? For example, is "Reliability" (fault tolerance/recovery) clearly distinguished from "Security" (resistance to malicious actors) and "Maintainability" (ease of fixing/modifying)? Would a machine learning model easily tell them apart based *only* on these texts?
4. Formatting: Is the definition a cohesive, well-structured, and fluid paragraph (no bullet points, no disjointed sentences)?

CORRECTION INSTRUCTIONS:
If any of the generated definitions fail one or more of these checks, you must act as the editor and rewrite them. Ensure the final definitions are robust, distinct, and perfectly aligned with the official standard, while maintaining the fluid paragraph constraint.

OUTPUT FORMAT:
First, provide a brief paragraph explaining your self-reflection process, explicitly mentioning which classes required adjustments and why (e.g., "I refined Reliability to better distinguish it from Security by emphasizing...").
Then, output the final, corrected list strictly as a JSON array of objects with the keys "class_name" and "class_definition".

Example Output Structure:
[Self-reflection explanation paragraph here]

[
    {
        "class_name": "Functional Suitability",
        "class_definition": "..."
    },
    ...
]
```

### PROMPT 3: Projects Definition (Persona + Few‑shot + Contextual Prompting)

```text
Act as a senior software architect and domain analyst specialized in software taxonomies, requirements engineering, and project conceptualization.
You are analyzing a provided dataset to generate a comprehensive suite of software projects.

INPUT DATA:
The attached CSV file containing the 'term' and 'hypernym' columns representing child-parent relationships.

Task:
Extract and analyze the hypernyms (parents) and their associated terms (children) from the CSV. Identify the parent categories that possess the most children and collectively span the entire, diverse spectrum of the software domain. Based strictly on this taxonomy analysis, generate exactly 35 diverse software projects.

Description:
The generated projects must ensure complete coverage of the software spectrum dictated by the CSV. They should range from representing highly specific nodes (terms with a single parent) to broad, cross-cutting concepts (terms sharing multiple parents). The goal is to create a universally representative dataset of modern and legacy software projects based on empirical taxonomy data.

Few-shot examples of project generation:

[FEW_SHOT_EXAMPLES]
1.
Project: Homeland Security Event Projection System
Description: A situational awareness desktop application designed for the Department of Homeland Security to monitor real-time event data and display it on large projection screens.

2.
Project: Real Estate PDA Assistant
Description: A mobile application designed for Personal Digital Assistants (PDAs), enabling real estate agents to access property information, client details, and listings on the go.

3.
Project: Nursing Clinical Scheduling System
Description: An academic scheduling application built to manage course scheduling and clinical practice rotations for nursing students and faculty.

4.
Project: Credit Card Holder Services Portal
Description: A web-based customer service and account management portal providing financial services, statement viewing, and account support for credit card holders.

5.
Project: Recycled Auto Parts Inventory System
Description: An inventory management system designed for salvage yards to track, categorize, and sell recycled automobile parts.

Instructions:

Step 1 — Taxonomy reasoning
Analyze the provided CSV relationships. Extract the root hypernyms and identify which parent nodes have the highest density of children. Explain how these central nodes can be categorized to cover the entire software spectrum (e.g., separating AI, web development, embedded systems, databases, etc.).

Step 2 — Coverage planning
Plan the distribution of the 35 projects. Describe how you will map the top hypernym categories to real-world project concepts to guarantee that both highly specialized terms and broad, multi-parent terms are represented in the final list.

Step 3 — Project generation
Generate 35 distinct software projects based on the planning from Step 2.

Constraints:

- Base the domains of the projects strictly on the broad hypernym categories extracted from the CSV.
- Ensure extreme semantic and domain diversity (do not make all 35 projects about web apps or all about AI).
- Project names must be professional and realistic.
- Descriptions must clearly define the system's purpose and implicitly tie back to the overarching taxonomy domains.
- Output exactly 35 projects.

Output format:

Projects:
1.
Project: [Project Name]
Description: [Project Description]

2.
Project: [Project Name]
Description: [Project Description]

...
35.
Project: [Project Name]
Description: [Project Description]

Give me only the output of the steps and the projects.
```

### PROMPT 4: Projects Validation (Persona + Self‑Reflection)

```text
You are a quality assurance specialist for software engineering datasets. Your task is to review the following list of 35 software projects, which was generated automatically, and perform a self‑reflection to validate its quality.

<INITIAL_PROJECT_LIST>

Follow these validation steps:
1. Check for diversity: ensure the projects cover at least 10 different domains (e.g., healthcare, finance, education, e‑commerce, logistics, AI/ML, cybersecurity, IoT, government, entertainment).
2. Verify realism: each project should be plausible and align with modern software development trends (post‑2020).
3. Detect duplicates: if any two projects are too similar in domain or purpose, replace one with a more distinct alternative.
4. Ensure completeness: all entries must have a clear project name and a concise description.

After your analysis, produce a refined list of 35 projects that meets the criteria above. If any changes are made, briefly explain them in a short paragraph before the final list. Output the final list as a JSON array of objects with keys "project" and "description".
```

### PROMPT 5: Projects Justification (Persona + Chain‑of‑Thought)

```text
You are a senior requirements engineer responsible for justifying the selection of projects used to build a high‑quality dataset. You have a validated list of 35 modern software projects. Now you must provide a chain‑of‑thought justification that explains why each project contributes to the diversity and representativeness of the dataset.

<VALIDATED_PROJECT_LIST>

For each project, write a brief justification (one or two sentences) that covers:
- The domain or industry sector.
- The type of system (e.g., web app, mobile, embedded, AI‑based, etc.).
- Why this project is relevant to modern requirements engineering (e.g., it involves complex stakeholder needs, regulatory compliance, ambiguous goals, or innovative technology).

After writing all justifications, output the final list again as a JSON array, this time including a "justification" field alongside "project" and "description". The output should be a single JSON array where each object contains:
{
  "project": "...",
  "description": "...",
  "justification": "..."
}
```

### PROMPT 6: Few-Shot Examples Generation (Persona + Chain of Thought)

```text
You are a senior requirements engineer with deep expertise in ISO/IEC 25010 and in writing software requirements for diverse systems. You know how to control two orthogonal dimensions: length (short vs. long) and clarity (consistent vs. ambiguous).

Your task is to generate 3 few‑shot example requirements for each of the four requirement types defined below. These examples will later be used as reference for generating a larger dataset.

QUALITY CLASS (ISO/IEC 25010)
Class name: [CLASS_NAME]
Definition: [CLASS_DEFINITION]

REQUIREMENT TYPES TO GENERATE:

1. **Short & Ambiguous**
   - Short: one sentence, typically 5–15 words.
   - Ambiguous: uses vague terms (e.g., "fast", "user‑friendly", "often", "appropriate", "as needed"), lacks measurable criteria, or has multiple interpretations.

2. **Long & Ambiguous**
   - Long: two or three sentences, 25–60 words.
   - Ambiguous: contains vague statements, weasel words, or missing details, but within a longer narrative.

3. **Short & Consistent**
   - Short: one sentence, 5–15 words.
   - Consistent: measurable, unambiguous, uses concrete terms (e.g., "within 2 seconds", "exactly three roles", "validates against regex").

4. **Long & Consistent**
   - Long: two or three sentences, 25–60 words.
   - Consistent: fully detailed, testable, leaves no room for misinterpretation, follows quality criteria (e.g., specific conditions, quantifiable metrics, clear scope).

INSTRUCTIONS:

Before writing the examples, think step by step:

1. What does this specific ISO/IEC 25010 quality class encompass? Identify typical system attributes, constraints, and features governed by this characteristic.
2. For **ambiguous** types: How are requirements related to this quality class often described vaguely in real life? (e.g., using subjective terms, lacking measurable thresholds).
3. For **consistent** types: What would a well‑written, testable requirement look like for this exact same quality class? (e.g., precise metrics, clear conditions, standard protocols).
4. For **short** types: Keep only the essential subject‑verb‑object. Avoid dependent clauses.
5. For **long** types: Add context, conditions, or exceptions while maintaining either ambiguity or consistency.

Then generate exactly 3 examples for each of the four types, ensuring they are all strictly related to the given quality class ([CLASS_NAME]).


OUTPUT FORMAT:

Return a valid JSON array with exactly 4 objects, one per type, in the following order:

[
  {
    "type": "short_ambiguous",
    "examples": [
      { "text": "example requirement", "explanation": "why it is short and ambiguous" }
    ]
  },
  {
    "type": "long_ambiguous",
    "examples": [
      { "text": "example requirement", "explanation": "..." }
    ]
  },
  {
    "type": "short_consistent",
    "examples": [
      { "text": "example requirement", "explanation": "..." }
    ]
  },
  {
    "type": "long_consistent",
    "examples": [
      { "text": "example requirement", "explanation": "..." }
    ]
  }
]

Each "examples" array must contain exactly 3 objects. The "explanation" field is mandatory and should briefly justify how the example meets the length and clarity criteria, as well as its relevance to the ISO class.
```
