import { Component, OnInit } from '@angular/core';
import * as d3 from "d3";
import { Plot } from '../../canonicals/Plot';
import { DataService } from '../../service/data-service.service';
import { PlotPoint } from 'src/app/canonicals/PlotPoint';
import { delay } from 'q';
import { Extent } from 'src/app/canonicals/Extent';

@Component({
  selector: 'app-visual',
  templateUrl: './visual.component.html',
  styleUrls: ['./visual.component.css']
})
export class VisualComponent implements OnInit {
  points: PlotPoint[] = [];
  window: Extent;
  liveWindow: Extent;

  constructor(
    private dataService: DataService) {
  }

  ngOnInit() {
    this.observeWindow();
    this.dataService.getPlot().then((response: PlotPoint[]) => {
      this.points = response;
    }).catch((error) => console.log(error));
  }

  observeWindow(): any {
    this.dataService.getWindow().subscribe((response: Extent) => {
      this.liveWindow = response;
    });
  }

  async showWindow() {
    this.window = null;
    await delay(1000);
    this.window = this.liveWindow;
  }
}
