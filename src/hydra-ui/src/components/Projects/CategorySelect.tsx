import { Select } from "antd";
import { useSelector } from "react-redux";
import { Category } from "../../api/TimeReporting/types";
import { selectAllCategories } from "../../store/categories";

interface Props {
  onChange: (value: number) => void;
  value: number;
  disabled?: boolean;
  placeholder: string;
}

export function CategorySelect({
  onChange,
  value,
  disabled,
  placeholder,
}: Props) {
  const categories = useSelector(selectAllCategories);

  return (
    <Select
      style={{ width: "100%" }}
      disabled={disabled}
      optionLabelProp="name"
      showSearch
      placeholder={placeholder}
      id="category_id"
      value={value}
      showArrow
      onChange={onChange}
      filterOption={(inputValue, option) => {
        return (
          option && option.name.toLowerCase().includes(inputValue.toLowerCase())
        );
      }}
    >
      {categories.map((category: Category) => (
        <Select.Option
          key={category.id}
          name={category.name}
          value={category.id}
        >
          <div className="select-option">{category.name}</div>
        </Select.Option>
      ))}
    </Select>
  );
}
