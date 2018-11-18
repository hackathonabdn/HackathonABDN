import { Component, OnInit } from '@angular/core';
import * as d3 from "d3";
import { Plot } from '../../canonicals/Plot';
import { DataService } from '../../service/data-service.service';
import { PlotPoint } from 'src/app/canonicals/PlotPoint';

@Component({
  selector: 'app-visual',
  templateUrl: './visual.component.html',
  styleUrls: ['./visual.component.css']
})
export class VisualComponent implements OnInit {
  points: PlotPoint[] = [];
  window: PlotPoint[] = [];

  constructor(
    private dataService: DataService) {
    this.observeWindow();
  }

  ngOnInit() {
    this.dataService.getPlot().then((response: PlotPoint[]) => {
      this.points = response;
    }).catch((error) => console.log(error));
  }

  observeWindow(): void {
    this.dataService.getWindow().subscribe((response: PlotPoint[]) => {
      this.window = response;
    });
  }
}
