export interface DFormValue {
    name: string;
    value: string;
}
export declare type DFormValues = Array<DFormValue>;
export interface Specification {
    args?: DFormValues;
    branch?: string;
    check_id: string;
    commit?: string;
    component: string;
    github_token?: string;
    height: string;
    path: string;
    repository: string;
    story: string;
    url_check_frame: string;
    width: string;
    dataPath: string;
}
