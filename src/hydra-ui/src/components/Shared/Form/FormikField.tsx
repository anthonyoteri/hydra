import { Checkbox, Form, Input, InputNumber } from "antd";
import { CheckboxProps } from "antd/lib/checkbox";
import { FormItemProps } from "antd/lib/form";
import { InputProps } from "antd/lib/input";
import { InputNumberProps } from "antd/lib/input-number";
import Select, { SelectProps } from "antd/lib/select";
import { SelectValue } from "antd/lib/tree-select";
import { Field, FieldProps } from "formik";
import React, { FC } from "react";
import { useTranslation } from "react-i18next";

export interface FormikFieldProps extends Omit<FormItemProps, "children"> {
  name: string;
  label?: string | React.ReactNode;
  required?: boolean;
  compact?: boolean;
  helpText?: string;
  validate?: (value: any) => undefined | string | Promise<any>;
}

export interface FormikFieldWrapperProps extends FormikFieldProps {
  extra?: React.ReactNode | "string";
  labelExtra?: React.ReactNode | "string";
  children: (
    props: FieldProps
  ) => React.ReactElement | React.ReactElement[] | null;
}

export const FormikField: FC<FormikFieldWrapperProps> = ({
  name,
  label,
  children,
  compact,
  required = false,
  className = "",
  style = undefined,
  helpText = null,
  extra = null,
  validate,
}) => {
  const { t } = useTranslation();

  return (
    <Field name={name} validate={validate}>
      {({ field, form, meta }: FieldProps) => {
        return (
          <Form.Item
            style={style}
            className={compact ? "form-field-compact " + className : className}
            required={required}
            htmlFor={name}
            label={label}
            extra={extra}
            validateStatus={meta.error && meta.touched ? "error" : ""}
            help={
              meta.error && meta.touched && typeof meta.error === "string"
                ? t(meta.error)
                : helpText
                ? t(helpText)
                : null
            }
          >
            {children({ field, form, meta })}
          </Form.Item>
        );
      }}
    </Field>
  );
};

type FormikFieldInputProps = FormikFieldProps & InputProps;

export const FormikFieldInput: FC<FormikFieldInputProps> = ({
  name,
  label,
  required,
  validate,
  helpText,
  ...rest
}) => {
  return (
    <FormikField
      name={name}
      label={label}
      required={required}
      validate={validate}
      helpText={helpText}
    >
      {({ field }) => (
        <Input
          {...field}
          value={field.value}
          onChange={field.onChange}
          name={name}
          id={name}
          {...rest}
        />
      )}
    </FormikField>
  );
};

type FormikFieldInputNumberProps = FormikFieldProps & InputNumberProps;

export const FormikFieldInputNumber: FC<FormikFieldInputNumberProps> = ({
  name,
  label,
  required,
  helpText,
  ...rest
}) => {
  return (
    <FormikField
      name={name}
      label={label}
      required={required}
      helpText={helpText}
    >
      {({ field, form: { setFieldValue } }) => (
        <InputNumber
          value={field.value}
          onChange={(value) => {
            setFieldValue(name, value);
          }}
          onBlur={(e) => field.onBlur(e)}
          name={name}
          id={name}
          {...rest}
        />
      )}
    </FormikField>
  );
};

type FormikFieldCheckboxProps = FormikFieldProps & CheckboxProps;

export const FormikFieldCheckbox: FC<FormikFieldCheckboxProps> = ({
  name,
  children,
  helpText,
  compact,
  ...rest
}) => {
  return (
    <FormikField name={name} helpText={helpText} compact={compact}>
      {({ field, form: { setFieldValue } }) => (
        <Checkbox
          {...rest}
          checked={field.value}
          onChange={(event) => setFieldValue(name, event.target.checked)}
        >
          {children}
        </Checkbox>
      )}
    </FormikField>
  );
};

type FormikFieldSelectProps = FormikFieldProps & SelectProps<SelectValue>;

export const FormikFieldSelect: FC<FormikFieldSelectProps> = ({
  name,
  label,
  validate,
  helpText,
  children,
  ...rest
}) => {
  return (
    <FormikField
      name={name}
      validate={validate}
      label={label}
      helpText={helpText}
    >
      {({ field, form }) => (
        <Select
          {...rest}
          value={field.value}
          onChange={(value: SelectValue) =>
            form.setFieldValue(field.name, value)
          }
        >
          {children}
        </Select>
      )}
    </FormikField>
  );
};
