import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { Plot } from '../canonicals/Plot';
import { PlotPoint } from '../canonicals/PlotPoint';
import { BehaviorSubject, Observable } from 'rxjs';
import { Extent } from '../canonicals/Extent';

@Injectable()
export class DataService {

  private readonly getPlotApi: string = `${environment.flaskPath}getplotdata`;
  private readonly retrieveMatchesApi: string = `${environment.flaskPath}retrieve`;
  private readonly windowSubj: BehaviorSubject<Extent>;

  constructor(
    private http: HttpClient) {
    this.windowSubj = new BehaviorSubject<Extent>({} as Extent);
  }

  async getPlot(wellName: string): Promise<PlotPoint[]> {
    return await this.http.get<Plot>(`${this.getPlotApi}/${wellName}`).toPromise().then((response: Plot) => {
      return response.depth.map((x, i) => {
        return {
          x: x,
          y: response.curve[i]
        } as PlotPoint;
      });
    }).catch((error) => {
      throw error;
    });
  }

  async retrieveMatches(wellName: string, fr: number, to: number): Promise<PlotPoint[][]> {
    return await this.http.get<Plot[]>(`${this.retrieveMatchesApi}/${wellName}/${fr}/${to}`).toPromise().then((response: Plot[]) => {
      return response.map(plot => {
        return plot.depth.map((x, i) => {
          return {
            x: x,
            y: plot.curve[i]
          } as PlotPoint;
        })
      })
    }).catch((error) => {
      throw error;
    });
  }

  getWindow(): Observable<Extent> {
    return this.windowSubj.asObservable();
  }

  setWindow(window: Extent): void {
    this.windowSubj.next(window);
  }
}
