import re
def __get_val_formula(row, dict_val):
  new_coord = ["{0}{1}".format(i, row) for i in dict_val["col"]]
  dict_val["val_list"][::2] = dict_val["base"]
  dict_val["val_list"][1::2] = new_coord
  formula_val = "".join(dict_val["val_list"])
  return formula_val

output_dict = {}
for idx, str_val in enumerate(['=E1-E1*0.15-J1', '=IF(K1&lt;0, TRUE, FALSE)', '=J1*22500+K1*3000']):
  base_str = re.split(r"\$?[A-Z]{1,3}\$?\d+", str_val)
  col_list = []
  for item in re.finditer(r"\$?([A-Z]{1,3})\$?\d+", str_val):
    col_list.append(item.group(1))
  output_dict[idx] = {}
  output_dict[idx]["base"] = base_str
  output_dict[idx]["col"] = col_list
  output_dict[idx]["val_list"] = [None]*(len(base_str) + len(col_list))

for row in range(2, 10):
  formula_val = __get_val_formula(row, output_dict[0])
  alert_val = __get_val_formula(row, output_dict[1])
  convert_val = __get_val_formula(row, output_dict[2])
  print(formula_val)
  print(alert_val)
  print(convert_val)

