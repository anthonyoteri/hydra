import { Select } from "antd";
import { useSelector } from "react-redux";
import { Project } from "../../api/TimeReporting/types";
import { selectAllProjects } from "../../store/projects";

interface Props {
  onChange: (value: number) => void;
  value: number;
  disabled?: boolean;
  placeholder: string;
}

export function ProjectSelect({
  onChange,
  value,
  disabled,
  placeholder,
}: Props) {
  const projects = useSelector(selectAllProjects);

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
