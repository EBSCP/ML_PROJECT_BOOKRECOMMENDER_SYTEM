import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MainComponent } from './Components/main/main.component';
import { SearchComponent } from './Components/search/search.component';
import { CategorizeComponent } from './Components/categorize/categorize.component';

const routes: Routes = [
  { path: '', component: MainComponent },
  { path: 'search', component: SearchComponent },
  {path: 'kategori',component: CategorizeComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
