
export interface DFormValue {
  name: string
  value: string
}

export type DFormValues = Array<DFormValue>

// BaseResult is the same as Specification in ss
export interface BaseResult {
  args?: DFormValues
  branch?: string
  check_id: string
  commit?: string
  component: string
  github_token?: string
  height: string
  name: string
  path: string
  repository: string
  story: string
  url_check_frame: string
  width: string
}