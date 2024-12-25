import json

def get_optimization_method(json_file, step_number):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    optimization_methods = data.get("OptimizationMethods", [])
    
    for method in optimization_methods:
        if method.get("step") == step_number:
            return method.get("Method"), method.get("Actions")
    
    return None, None



def generate_suggestions_text(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    optimization_methods = data.get("OptimizationMethods", [])
    suggestions = "请你根据以下修改建议，逐步尝试。"
    
    for method in optimization_methods:
        step_number = method.get("step")
        method_name = method.get("Method")
        actions = method.get("Actions", [])
        
        suggestions += f"\n\n第{step_number}步：{method_name}"
        for action in actions:
            suggestions += f"\n- {action}"
    
    return suggestions


if __name__ == "__main__":

    # demo1
    # json_file = 'suggestion.json'
    # step_number = 1
    # method, actions = get_optimization_method(json_file, step_number)

    # if method and actions:
    #     print(f"Method: {method}")
    #     print("Actions:")
    #     for action in actions:
    #         print(f"- {action}")
    # else:
    #     print(f"No optimization method found for step {step_number}")

    # demo2
    json_file = 'suggestion/suggestion.json'
    suggestions_text = generate_suggestions_text(json_file)
    print(suggestions_text)