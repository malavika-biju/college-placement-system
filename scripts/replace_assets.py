import re
from pathlib import Path
p = Path(r"c:\Django_projects\catalystProject\templates\Admin\edit_district.html")
s = p.read_text(encoding='utf-8')
# Replace any attribute value that contains ../assets/... with Django static tag
pattern = re.compile(r'(["\'])(\.\./assets/([^"\']+))\1')
new = pattern.sub(lambda m: f'\"{{% static \'Admin/assets/{m.group(3)}\' %}}\"' if m.group(1)=='"' else f"'{{% static \'Admin/assets/{m.group(3)}\' %}}'", s)
# Also replace any remaining data-assets-path="../assets/" occurrences
new = new.replace('data-assets-path="../assets/"', 'data-assets-path="{% static \"Admin/assets/\" %}"')
# Write back
p.write_text(new, encoding='utf-8')
print('Replacements complete')
