interface ErrorData {
    aws?: string;
    branch?: string;
    clone?: string;
    commit?: string;
    comp?: string;
    frame?: string;
    install?: string;
    storycap?: string;
}
export interface MessageResult {
    MAE?: string;
    code_paths?: Array<string>;
    code_size?: number;
    code_snippets?: Array<string>;
    completed_at?: number;
    created_at?: number;
    url_blue_difference?: string;
    url_check_frame: string;
    url_gray_difference?: string;
    url_screenshot?: string;
}
export interface MessageData {
    check_id: string;
    error?: ErrorData;
    message: string;
    results?: MessageResult;
    step: number;
    step_count: number;
}
export interface CliResult {
    success: boolean;
    result?: MessageData;
    message?: string;
}
export declare const PASS_SCORE = 50;
export {};
