import json
import os
from pathlib import Path

# ----------------------------------------------------------------------
PROMPT_SHORT_AMBIGUOUS = """You are a senior requirements engineer with deep expertise in ISO/IEC 25010. Your task is to generate 10 SHORT and AMBIGUOUS requirements for a given software project and quality class.

Definition of "short and ambiguous":
- Short: strictly a single sentence containing between 10 and 20 words.
- Ambiguous: lacks sufficient context or explicit boundary conditions, introducing controlled subjectivity. While it must primarily reflect the target quality class (70-80% of the core intent), its vague wording should allow it to be partially interpreted as a secondary class (20-30% overlap). Use subjective terms (e.g., "adequate", "seamless", "fast", "intuitive") without measurable metrics.

Below are a few examples that illustrate the desired style. Use them as reference (few-shot) for tone and  structure.

[FEW_SHOT_EXAMPLES]

Now, for the following project and quality class, generate 10 new requirements that follow the same short & ambiguous style.

Project name: [PROJECT_NAME]
Project description: [PROJECT_DESCRIPTION]

Quality class (ISO/IEC 25010):
Class name: [CLASS_NAME]
Definition: [CLASS_DEFINITION]

Chain-of-Thought (think before you write):
1. Consider the project context: what are typical user interactions, system functions, or quality concerns?
2. Formulate the core intent based on the target Quality class.
3. Inject controlled ambiguity: rewrite the intent using vague wording that creates a slight semantic overlap with another class, while maintaining the primary class as dominant.
4. Verify constraint: Ensure each requirement is exactly one sentence and strictly between 10 and 20 words long.

Output format:

Requirements:
1.
2.
3.
...
10.

Ensure all requirements are directly related to the given quality class and the specific project."""

PROMPT_LONG_AMBIGUOUS = """You are a senior requirements engineer with deep expertise in ISO/IEC 25010. Your task is to generate 10 LONG and AMBIGUOUS requirements for a given software project and quality class.

Definition of "long and ambiguous":
- Long: one or two sentences, strictly containing between 25 and 50 words total.
- Ambiguous: lacks sufficient context or explicit boundary conditions, introducing controlled subjectivity. While it must primarily reflect the target quality class (70-80% of the core intent), its verbose but vague wording should allow it to be partially interpreted as a secondary class (20-30% overlap). Use subjective terms, unquantified scenarios, or open-ended exceptions.

Below are a few examples that illustrate the desired style. Use them as reference (few-shot) for tone, structure, and level of ambiguity.

[FEW_SHOT_EXAMPLES]

Now, for the following project and quality class, generate 10 new requirements that follow the same long & ambiguous style.

Project name: [PROJECT_NAME]
Project description: [PROJECT_DESCRIPTION]

Quality class (ISO/IEC 25010):
Class name: [CLASS_NAME]
Definition: [CLASS_DEFINITION]

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

Ensure all requirements are directly related to the given quality class and the specific project."""

PROMPT_SHORT_CONSISTENT = """You are a senior requirements engineer with deep expertise in ISO/IEC 25010. Your task is to generate 10 SHORT and CONSISTENT requirements for a given software project and quality class.

Definition of "short and consistent":
- Short: strictly a single sentence containing between 10 and 20 words.
- Consistent: presents a single unavoidable interpretation and is directly verifiable. It must have exclusive categorical alignment with the target class, meaning there is zero semantic overlap with other classes. Use precise language and clear conditions (e.g., specific actions, exact constraints, or logical/functional tests).

Below are a few examples that illustrate the desired style. Use them as reference (few-shot) for tone and structure.

[FEW_SHOT_EXAMPLES]

Now, for the following project and quality class, generate 10 new requirements that follow the same short & consistent style.

Project name: [PROJECT_NAME]
Project description: [PROJECT_DESCRIPTION]

Quality class (ISO/IEC 25010):
Class name: [CLASS_NAME]
Definition: [CLASS_DEFINITION]

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

Ensure all requirements are directly related to the given quality class and the specific project."""

PROMPT_LONG_CONSISTENT = """You are a senior requirements engineer with deep expertise in ISO/IEC 25010. Your task is to generate 10 LONG and CONSISTENT requirements for a given software project and quality class.

Definition of "long and consistent":
- Long: one or two sentences, strictly containing between 25 and 50 words total.
- Consistent: presents a single unavoidable interpretation and is directly verifiable. It must have exclusive categorical alignment with the target class, meaning there is zero semantic overlap with other classes. Use fully detailed phrasing, clear scope, and precise conditions, preconditions, or metrics.

Below are a few examples that illustrate the desired style. Use them as reference (few-shot) for tone and structure. 

[FEW_SHOT_EXAMPLES]

Now, for the following project and quality class, generate 10 new requirements that follow the same long & consistent style.

Project name: [PROJECT_NAME]
Project description: [PROJECT_DESCRIPTION]

Quality class (ISO/IEC 25010):
Class name: [CLASS_NAME]
Definition: [CLASS_DEFINITION]

Chain-of-Thought (think before you write):
1. Consider the project context: what are typical user interactions, system functions, or quality concerns?
2. Formulate the requirement with extensive detail (context, preconditions, or thresholds), ensuring exclusive alignment with the target class and zero semantic overlap.
3. Verify constraint: Ensure each requirement is one or two sentences and strictly totals between 25 and 50 words.

Output format:

Requirements:
1.
2.
3.
...
10.

Ensure all requirements are directly related to the given quality class and the specific project."""

TEMPLATES = {
    "short_ambiguous": PROMPT_SHORT_AMBIGUOUS,
    "long_ambiguous": PROMPT_LONG_AMBIGUOUS,
    "short_consistent": PROMPT_SHORT_CONSISTENT,
    "long_consistent": PROMPT_LONG_CONSISTENT
}

# ----------------------------------------------------------------------
def load_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {filepath}")
        return []

projects = load_json('projects.json')
classes = load_json('classes.json')
few_shots_data = load_json('few_shot_samples.json')

# ----------------------------------------------------------------------
few_shots_dict = {}

for item in few_shots_data:
    c_name = item.get("class_name")
    few_shots_dict[c_name] = {}
    
    for sample_group in item.get("samples", []):
        p_type = sample_group.get("type")
        examples = sample_group.get("examples", [])
        
        formatted_examples = "\n".join([f"{i+1}. {ex}" for i, ex in enumerate(examples)])
        few_shots_dict[c_name][p_type] = formatted_examples

# ----------------------------------------------------------------------
output_root = Path('dist')
output_root.mkdir(exist_ok=True)

data_root = Path('data')
data_root.mkdir(exist_ok=True)

# Iterar sobre los proyectos (project1, project2, ...)
for proj_idx, project_data in enumerate(projects, start=1):
    project_name = project_data['project']
    project_desc = project_data['description']
    
    # Crear directorio del proyecto
    project_folder = output_root / f"project{proj_idx}"
    project_folder.mkdir(exist_ok=True)

    # Crear directorio de datos del proyecto
    data_project_folder = data_root / f"project{proj_idx}"
    data_project_folder.mkdir(exist_ok=True)

    # Iterar sobre las clases (01, 02, ...)
    for class_idx, class_data in enumerate(classes, start=1):
        class_name = class_data['class_name']
        class_def = class_data['class_definition']
        
        # Formatear el nombre de la carpeta de la clase (ej: 01_functional_suitability_prompts)
        safe_class_name = class_name.lower().replace(' ', '_')
        class_folder_name = f"{class_idx:02d}_{safe_class_name}_prompts"

        class_folder = project_folder / class_folder_name
        class_folder.mkdir(exist_ok=True)

        data_class_folder = data_project_folder / class_folder_name
        data_class_folder.mkdir(exist_ok=True)

        # Si no hay few-shots para esta clase, lanzar un aviso, pero continuar
        if class_name not in few_shots_dict:
            print(f"Warning: No se encontraron few-shots para la clase '{class_name}'.")
            continue

        # Generar los archivos para cada tipo de prompt ("short_ambiguous", "long_ambiguous")
        for prompt_type, template_str in TEMPLATES.items():
            
            # Obtener los ejemplos formateados para este tipo
            examples_text = few_shots_dict[class_name].get(prompt_type, "No examples provided.")
            
            # Reemplazar los placeholders en el template
            prompt_content = template_str \
                .replace("[PROJECT_NAME]", project_name) \
                .replace("[PROJECT_DESCRIPTION]", project_desc) \
                .replace("[CLASS_NAME]", class_name) \
                .replace("[CLASS_DEFINITION]", class_def) \
                .replace("[FEW_SHOT_EXAMPLES]", examples_text)
            
            # Escribir el archivo
            output_file = class_folder / f"{prompt_type}.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(prompt_content)

            data_file = data_class_folder / f"{prompt_type}_response.txt"
            with open(data_file, 'w', encoding='utf-8') as f:
                pass # La instrucción 'pass' asegura que el archivo se cree vacío
                
            print(f"Generado: {output_file} | Archivo vacío: {data_file}")
                
print("\nProceso terminado exitosamente.")
