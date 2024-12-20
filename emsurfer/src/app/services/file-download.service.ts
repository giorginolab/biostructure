import { Injectable } from "@angular/core";

@Injectable({
  providedIn: "root"
})
export class FileDownloadService {
  constructor() {}

  getSearchResultFilePath(fileId: number) {
    return "http://localhost:3001/results/result.hit";
  }

  getBenchmarkResultCompressedFilePath(fileId: number) {
    return "assets/test_files/test_result.hit";
  }
}
