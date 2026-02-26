import ast


def list_keywords_with_decorators(file_path):
    try:
        with open(file_path, 'r') as file:
            node = ast.parse(file.read(), filename=file_path)
            found_keywords = []

            for n in ast.walk(node):  # Tüm AST düğümlerini dolaş
                if isinstance(n, ast.FunctionDef):
                    # Fonksiyon dekoratörlerini kontrol et
                    for decorator in n.decorator_list:
                        # @keyword dekoratörünü bul
                        if isinstance(decorator, ast.Name) and decorator.id == 'keyword':
                            found_keywords.append({
                                'function_name': n.name,
                                'decorator': 'keyword',
                                'line': n.lineno
                            })
                        # @keyword("aaaa") şeklindeki dekoratörleri bul
                        elif isinstance(decorator, ast.Call):
                            if isinstance(decorator.func, ast.Name) and decorator.func.id == 'keyword':
                                # Dekoratörün argümanlarını al
                                keyword_value = None
                                if decorator.args:
                                    if isinstance(decorator.args[0], ast.Constant):
                                        keyword_value = decorator.args[0].value
                                    elif isinstance(decorator.args[0], ast.Str):  # Python 3.7 ve öncesi
                                        keyword_value = decorator.args[0].s

                                found_keywords.append({
                                    'function_name': n.name,
                                    'decorator': 'keyword',
                                    'keyword_value': keyword_value,
                                    'line': n.lineno
                                })

            return found_keywords

    except FileNotFoundError:
        print(f"{file_path} bulunamadı.")
        return []
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return []


# Alternatif ve daha kapsamlı bir versiyon
def list_detailed_keywords(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            node = ast.parse(content, filename=file_path)

            keywords = []
            classes = []

            for n in node.body:
                # Sınıfları bul
                if isinstance(n, ast.ClassDef):
                    class_info = {
                        'name': n.name,
                        'line': n.lineno,
                        'methods': []
                    }

                    # Sınıf içindeki metodları bul
                    for item in n.body:
                        if isinstance(item, ast.FunctionDef):
                            method_info = {
                                'name': item.name,
                                'line': item.lineno,
                                'decorators': []
                            }

                            # Metod dekoratörlerini kontrol et
                            for decorator in item.decorator_list:
                                if isinstance(decorator, ast.Name) and decorator.id == 'keyword':
                                    method_info['decorators'].append({
                                        'type': 'keyword',
                                        'value': None
                                    })
                                elif isinstance(decorator, ast.Call):
                                    if isinstance(decorator.func, ast.Name) and decorator.func.id == 'keyword':
                                        # Keyword değerini al
                                        keyword_value = None
                                        if decorator.args:
                                            if hasattr(decorator.args[0], 'value'):
                                                keyword_value = decorator.args[0].value
                                            elif hasattr(decorator.args[0], 's'):
                                                keyword_value = decorator.args[0].s

                                        method_info['decorators'].append({
                                            'type': 'keyword',
                                            'value': keyword_value
                                        })

                            if method_info['decorators']:  # Sadece keyword dekoratörü olan metodları ekle
                                class_info['methods'].append(method_info)

                    if class_info['methods']:  # Keyword dekoratörlü metod varsa sınıfı ekle
                        classes.append(class_info)

                # Doğrudan fonksiyonları bul
                elif isinstance(n, ast.FunctionDef):
                    func_info = {
                        'name': n.name,
                        'line': n.lineno,
                        'decorators': []
                    }

                    for decorator in n.decorator_list:
                        if isinstance(decorator, ast.Name) and decorator.id == 'keyword':
                            func_info['decorators'].append({
                                'type': 'keyword',
                                'value': None
                            })
                        elif isinstance(decorator, ast.Call):
                            if isinstance(decorator.func, ast.Name) and decorator.func.id == 'keyword':
                                keyword_value = None
                                if decorator.args:
                                    if hasattr(decorator.args[0], 'value'):
                                        keyword_value = decorator.args[0].value
                                    elif hasattr(decorator.args[0], 's'):
                                        keyword_value = decorator.args[0].s

                                func_info['decorators'].append({
                                    'type': 'keyword',
                                    'value': keyword_value
                                })

                    if func_info['decorators']:
                        keywords.append(func_info)

            return {'functions': keywords, 'classes': classes}

    except FileNotFoundError:
        print(f"{file_path} bulunamadı.")
        return {'functions': [], 'classes': []}
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return {'functions': [], 'classes': []}


# Kullanım
file_path = 'C:\\Users\\user\\PycharmProjects\\QA_Lab_python\\pages\\GeekPage.py'

# Basit versiyon
simple_result = list_keywords_with_decorators(file_path)
print("Basit keyword listesi:")
for item in simple_result:
    if 'keyword_value' in item and item['keyword_value']:
        print(f"{item['function_name']} - @keyword({item['keyword_value']}) (satır {item['line']})")
    else:
        print(f"{item['function_name']} - @keyword (satır {item['line']})")

print("\n" + "=" * 50 + "\n")

# Detaylı versiyon
detailed_result = list_detailed_keywords(file_path)

print("Sınıflardaki keyword metodları:")
for class_info in detailed_result['classes']:
    print(f"\nSınıf: {class_info['name']}")
    for method in class_info['methods']:
        for dec in method['decorators']:
            if dec['value']:
                print(f"  - {method['name']} -> @keyword({dec['value']})")
            else:
                print(f"  - {method['name']} -> @keyword")

print("\nDoğrudan fonksiyonlardaki keywordler:")
for func in detailed_result['functions']:
    for dec in func['decorators']:
        if dec['value']:
            print(f"- {func['name']} -> @keyword({dec['value']})")
        else:
            print(f"- {func['name']} -> @keyword")