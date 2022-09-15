export interface DFormValue {
    name: string;
    value: string;
}
export declare type DFormValues = Array<DFormValue>;
export interface BaseResult {
    args?: DFormValues;
    branch?: string;
    check_id: string;
    commit?: string;
    component: string;
    github_token?: string;
    height: string;
    name: string;
    path: string;
    repository: string;
    story: string;
    url_check_frame: string;
    width: string;
}
