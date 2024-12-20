import { ModuleWithProviders } from "@angular/core";
import { Routes, RouterModule } from "@angular/router";
import { SearchFormComponent } from "./components/search-form/search-form.component";
import { SearchResultComponent } from "./components/search-result/search-result.component";
import { BenchmarkComponent } from "./components/benchmark/benchmark.component";
import { BenchmarkResultsComponent } from "./components/benchmark-results/benchmark-results.component";
import { HomeComponent } from "./components/home/home.component";
import { ReferenceComponent } from "./components/reference/reference.component";
import { ContactComponent } from "./components/contact/contact.component";
import { ZernikeDescriptorsModuleComponent } from "./components/zernike-descriptors-module/zernike-descriptors-module.component";
import { UserRolesComponent } from "./components/user-roles/user-roles.component";
import { SearchHistoryComponent } from "./components/search-history/search-history.component";
import { TutorialPageComponent } from "./components/tutorial-page/tutorial-page.component";
import { ParametersPanelComponent } from "./components/parameters-panel/parameters-panel.component";

export const router: Routes = [
  {
    path: "",
    redirectTo: "home",
    pathMatch: "full"
  },
  {
    path: "search",
    component: SearchFormComponent
  },
  {
    path: "result/:emdbId",
    component: SearchResultComponent
  },
  {
    path: "result/emMap",
    component: SearchResultComponent
  },
  {
    path: "benchmark",
    component: BenchmarkComponent
  },
  {
    path: "benchmark/results",
    component: BenchmarkResultsComponent
  },
  {
    path: "home",
    component: HomeComponent
  },
  {
    path: "reference",
    component: ReferenceComponent
  },
  {
    path: "contact",
    component: ContactComponent
  },
  {
    path: "zernike",
    component: ZernikeDescriptorsModuleComponent
  },
  {
    path: "admin/changeUserRole",
    component: UserRolesComponent
  },
  {
    path: "history",
    component: SearchHistoryComponent
  },
  {
    path: "admin/parameters",
    component: ParametersPanelComponent
  },
  {
    path: "tutorial",
    component: TutorialPageComponent
  }
];

export const routes: ModuleWithProviders = RouterModule.forRoot(router);
