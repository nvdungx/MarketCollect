import re

temp = re.search(r"[A-Z]{1,2}\d{1,2}", '=IF((E1-(E1*0.15+J1))&lt;0, TRUE, FALSE)')
pass