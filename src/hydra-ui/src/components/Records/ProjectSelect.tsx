import { Select } from "antd";
import { useSelector } from "react-redux";
import { Category, Project } from "../../api/TimeReporting/types";
import { selectProjectsForCategory } from "../../store/projects";
import { ApplicationState } from "../../store/rootReducer";

interface Props {
  category?: Category;
  onChange: (value: number) => void;
  value: number;
  disabled?: boolean;
  placeholder: string;
}

export function ProjectSelect({
  category,
  onChange,
  value,
  disabled,
  placeholder,
}: Props) {
  const projects = useSelector((state: ApplicationState) =>
    selectProjectsForCategory(state, category?.id)
  );

  return (
    <Select
      style={{ width: "100%" }}
      disabled={disabled}
      optionLabelProp="name"
      showSearch
      placeholder={placeholder}
      id="project_id"
      value={value}
      showArrow
      onChange={onChange}
      filterOption={(inputValue, option) => {
        return (
          option && option.name.toLowerCase().includes(inputValue.toLowerCase())
        );
      }}
    >
      {projects.map((project: Project) => (
        <Select.Option key={project.id} name={project.name} value={project.id}>
          <div className="select-option">{project.name}</div>
        </Select.Option>
      ))}
    </Select>
  );
}
