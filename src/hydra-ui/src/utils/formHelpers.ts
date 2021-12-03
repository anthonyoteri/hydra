import { FormikErrors, FormikValues } from "formik";
import { ApiError, ErrorItem } from "./../api/errors";

type FormErrorContainer<T extends FormikValues> = {
  formErrors: FormikErrors<T> | undefined;
  error: ApiError;
};

export const parseErrors = <T extends FormikValues>(
  err: ApiError
): FormErrorContainer<T> => {
  const formErrors: FormikErrors<T> = {};

  if (err.type !== "server") {
    return { formErrors: undefined, error: err };
  }

  const filtered = err.errors.map((e: ErrorItem) => {
    if (e.field) {
      if (e.field === "__all__") {
        delete e.field;
        return e;
      }
      const k = e.field as keyof T;
      formErrors[k] = e.message as any;
      return null;
    }
    return e;
  });

  return {
    formErrors,
    error: {
      ...err,
      errors: filtered.filter((e: ErrorItem | null) => e) as ErrorItem[],
    },
  };
};

export type FormStatus =
  | "pending"
  | "saving"
  | "completed"
  | "cancelled"
  | "error";
