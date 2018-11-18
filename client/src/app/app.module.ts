import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms'
import { HttpClientModule } from '@angular/common/http';
import { AppComponent } from './components/app/app.component';
import { VisualComponent } from './components/visual/visual.component';
import { DataService } from './service/data-service.service';
import { PlotComponent } from './components/plot/plot.component';

@NgModule({
  declarations: [
    AppComponent,
    VisualComponent,
    PlotComponent
  ],
  imports: [
    HttpClientModule,
    BrowserModule,FormsModule 
  ],
  providers: [DataService],
  bootstrap: [AppComponent]
})
export class AppModule { }
