import { useTranslation } from "react-i18next";
import { Modal } from "antd";
import { Formik, FormikHelpers } from "formik";
import { FC, useState } from "react";
import { Category, CategoryDraft } from "../../../api/TimeReporting";
import { CategoryForm, CategoryFormData } from "./CategoryForm";
import useModalForm from "../../../hooks/useModalForm";
import { parseErrors } from "../../../utils/formHelpers";
import { ModalFormFooter } from "../../Shared/ModalFormFooter";
import { ModalTitle } from "../../Shared/ModalTitle";
import { AppstoreOutlined } from "@ant-design/icons";
import { FormError } from "../../Shared/Form/FormError";

interface Props {
  type: "create" | "update";
  onOk: (category: Category) => Promise<any>;
  onComplete: () => void;
  onCancel: () => void;
  category: CategoryDraft;
}

export const CategoryDialog: FC<Props> = (props: Props) => {
  const { t } = useTranslation();
  const { onOk, onComplete, onCancel, type } = props;
  const [formData] = useState<CategoryFormData>({
    name: props.category.name,
    description: props.category.description,
  });
  const { isVisible, isSaving, error, setStatus, setError, handleAfterClose } =
    useModalForm({ onCancel: onCancel, onComplete: onComplete });

  const handleCancel = () => {
    setStatus("cancelled");
  };

  const compileCategory = (formData: CategoryFormData): Category => {
    return {
      name: formData.name,
      description: formData.description,
    } as Category;
  };

  const handleSubmit = async (
    category: CategoryFormData,
    formikHelpers: FormikHelpers<CategoryFormData>
  ) => {
    setStatus("saving");
    setError(null);

    try {
      await onOk(compileCategory(category));
      setStatus("completed");
    } catch (err: any) {
      const { formErrors, error } = parseErrors<CategoryFormData>(err);
      if (err.type === "server") {
        formErrors && formikHelpers.setErrors(formErrors);
        setError(err);
      } else {
        setError(error);
      }
      setStatus("error");
    }
  };

  const Footer = (
    <ModalFormFooter
      formName="categoryForm"
      onCancel={handleCancel}
      isLoading={isSaving}
      submitButtonText={
        type === "create" ? t("common.create") : t("common.saveChanges")
      }
    />
  );

  return (
    <Modal
      title={
        <ModalTitle
          icon={<AppstoreOutlined />}
          title={
            type === "create" ? t("common.createNew") : props.category.name
          }
          subtitle={t("configuration.categories.createDialog.subTitle")}
        />
      }
      width={640}
      visible={isVisible}
      confirmLoading={isSaving}
      onCancel={handleCancel}
      footer={Footer}
      maskClosable={false}
      afterClose={handleAfterClose}
    >
      <Formik initialValues={formData} onSubmit={handleSubmit}>
        {(props) => <CategoryForm formik={props} />}
      </Formik>

      <FormError error={error} />
    </Modal>
  );
};
